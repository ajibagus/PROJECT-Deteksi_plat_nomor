import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import numpy as np
from matplotlib import pyplot as plt
import cv2
import easyocr
import csv
import uuid
import mysql.connector
from mysql.connector import Error


def get_frame():
  CUSTOM_MODEL_NAME = 'my_ssd_mobnet_v2_320' 
  LABEL_MAP_NAME = 'label_map.pbtxt'

  paths = {
      'APIMODEL_PATH': os.path.join('Tensorflow','models'),
      'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace','annotations'),
      'IMAGE_PATH': os.path.join('Tensorflow', 'workspace','images'),
      'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME), 
  }

  files = {
      'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
      'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
  }
  # Load pipeline config and build a detection model
  configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
  detection_model = model_builder.build(model_config=configs['model'], is_training=False)

  # Restore checkpoint
  ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
  ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-11')).expect_partial()

  @tf.function
  def detect_fn(image):
      image, shapes = detection_model.preprocess(image)
      prediction_dict = detection_model.predict(image, shapes)
      detections = detection_model.postprocess(prediction_dict, shapes)
      return detections

  category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
  detection_threshold = 0.8
  region_threshold = 0.02
  def filter_text(region, ocr_result, region_threshold):
    rectangle_size = region.shape[0]*region.shape[1]
    
    plate = [] 
    for result in ocr_result:
        length = np.sum(np.subtract(result[0][1], result[0][0]))
        height = np.sum(np.subtract(result[0][2], result[0][1]))
        
        if length*height / rectangle_size > region_threshold:
            plate.append(result[1])
    return plate

   
  def ocr_it(image, detections, detection_threshold, region_threshold):
    
    # Scores, boxes and classes above threhold
    scores = list(filter(lambda x: x> detection_threshold, detections['detection_scores']))
    boxes = detections['detection_boxes'][:len(scores)]
    classes = detections['detection_classes'][:len(scores)]
    
    # Full image dimensions
    width = image.shape[1]
    height = image.shape[0]
    
    # Apply ROI filtering and OCR
    for idx, box in enumerate(boxes):
        roi = box*[height, width, height, width]
        region = image[int(roi[0]):int(roi[2]),int(roi[1]):int(roi[3])]
        reader = easyocr.Reader(['en'])
        ocr_result = reader.readtext(region)
        
        text = filter_text(region, ocr_result, region_threshold)
        plat = (''.join(map(str, text)))
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='big_project',
                                         user='root',
                                         password='')

    
            cursor = connection.cursor()
            #validate = cursor.execute("SELECT * FROM karyawan WHERE plat_nomor = %s", ( plat ))

            if (plat==''):
                print("plat kosong")
            # elif (validate==True):
            #     if(cursor.execute("SELECT * FROM laporan_masuk where no_plat = %s",(plat))):
            #         cursor.execute("INSERT INTO laporan_keluar VALUES (%s, %s, %s)", ('', plat, ''))
            #     else:
            #         cursor.execute("INSERT INTO laporan_masuk VALUES (%s, %s, %s)", ('', plat, ''))
            # elif (validate==False):
            #     if(cursor.execute("SELECT * FROM laporan_masuk where no_plat = %s",(plat))):
            #         cursor.execute("INSERT INTO laporan_keluar VALUES (%s, %s, %s)", ('', plat, ''))
            #     else:
            #         cursor.execute("INSERT INTO laporan_masuk VALUES (%s, %s, %s)", ('', plat, ''))
            else:
                cursor.execute("INSERT INTO hasil_scan VALUES (%s, %s)", ('',plat))
                connection.commit()
                print(cursor.rowcount, "Satu kolom telah ditambhakna")

        except mysql.connector.Error as error:
            print("Failed to insert record into MySQL table {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
        
        #plt.imshow(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
        #plt.show()
        print(plat)
        return plat, region

  
  def save_results(plat, region, csv_filename, folder_path):
    img_name = '{}.jpg'.format(uuid.uuid1())
    
    cv2.imwrite(os.path.join(folder_path, img_name), region)
    
    with open(csv_filename, mode='a', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([img_name, text])
        csv_writer.writerow(text)
    


  cap = cv2.VideoCapture(0)
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

  while cap.isOpened(): 
      ret, frame = cap.read()
      frame = cv2.resize(frame,(600, 400))
      #frame = cv2.resize(frame,(500, 400))
      image_np = np.array(frame)
      
      input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
      detections = detect_fn(input_tensor)
      
      num_detections = int(detections.pop('num_detections'))
      detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
      detections['num_detections'] = num_detections

      # detection_classes should be ints.|
      detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

      label_id_offset = 1
      image_np_with_detections = image_np.copy()

      #data = detections['detection_classes']+label_id_offset

      viz_utils.visualize_boxes_and_labels_on_image_array(
                  image_np_with_detections,
                  detections['detection_boxes'],
                  #data,
                  detections['detection_classes']+label_id_offset,
                  detections['detection_scores'],
                  category_index,
                  #print(category_index[data[0]]['name']),
                  use_normalized_coordinates=True,
                  max_boxes_to_draw=5,
                  min_score_thresh=.8,
                  agnostic_mode=False)

      try: 
            plat, region = ocr_it(image_np_with_detections, detections, detection_threshold, region_threshold)
            #save_results(text, region, 'realtimeresults.csv', 'Detection_Images')
            save_results(plat)
      except:
            pass

      ret, jpeg = cv2.imencode('.jpg', image_np_with_detections)
      frame = jpeg.tobytes()
      yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')