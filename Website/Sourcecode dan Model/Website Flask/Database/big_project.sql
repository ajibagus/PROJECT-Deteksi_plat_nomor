-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 17, 2022 at 12:25 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `big_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `email`, `username`, `password`) VALUES
(1, 'test@email.com', 'test', '123456'),
(3, 'karyawan@gmail.com', 'nurlaela', '1234'),
(4, 'ajibgs46@gmail.com', 'ajibgs', '12345678');

-- --------------------------------------------------------

--
-- Table structure for table `hasil_scan`
--

CREATE TABLE `hasil_scan` (
  `id_scan` int(11) NOT NULL,
  `plat_no` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hasil_scan`
--

INSERT INTO `hasil_scan` (`id_scan`, `plat_no`) VALUES
(25, 'G 5678 AF');

--
-- Triggers `hasil_scan`
--
DELIMITER $$
CREATE TRIGGER `hasilscan` AFTER INSERT ON `hasil_scan` FOR EACH ROW insert into laporan_masuk(
        id_masuk, 
        no_plat, 
        waktu,
        id_scan
    )
    values(
        id_masuk,
        new.plat_no,
        CURRENT_TIMESTAMP(),
        new.id_scan
    )
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

CREATE TABLE `karyawan` (
  `id_krywn` int(11) NOT NULL,
  `nipy` varchar(15) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `plat_nomor` varchar(15) NOT NULL,
  `pass` varchar(50) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`id_krywn`, `nipy`, `nama`, `plat_nomor`, `pass`, `status`) VALUES
(3, '01.001.120', 'Aji', 'G6876WJG', 'admin', 'Dosen'),
(6, '01.001.100', 'Shin', 'G7890R', 'G7890RF', 'Dosen'),
(31, '01.001.120', 'opwm', 'G1256HG', 'G1256GH', 'Dosen'),
(33, '01.001.013', 'Fikriyah Khairunnisa', 'G5690RE', 'G5690RE', 'Karyawan'),
(37, '01.004.004', 'Diana', 'G7890AC', 'G7890AC', 'Dosen'),
(38, '01.003.003', 'Deni Saputra', 'G7890AD', 'G7890AD', 'Dosen'),
(39, '01.007.007', 'Rizki Febrianti', 'G7890AE', 'G7890AE', 'Karyawan'),
(41, '01.002.003', 'Fabillah', 'G7890AC', 'G7890AC', 'Karyawan'),
(42, '01.003.004', 'Muhamad Rizki', 'G7890AG', 'G7890AG', 'Dosen'),
(43, '01.001.009', 'Maya', 'G7890AQ', 'G7890AQ', 'Karyawan'),
(44, '01.001.008', 'Elannggggg', 'G1111C', 'G1111C', 'Karyawan'),
(45, '01.005.003', 'Essy Nur Jannah', 'G7890AE', 'G7890AE', 'Karyawan');

-- --------------------------------------------------------

--
-- Stand-in structure for view `keluar`
-- (See below for the actual view)
--
CREATE TABLE `keluar` (
`nama` varchar(50)
,`no_plat` varchar(20)
,`waktu` timestamp
,`keterangan` varchar(20)
);

-- --------------------------------------------------------

--
-- Table structure for table `laporan_keluar`
--

CREATE TABLE `laporan_keluar` (
  `id_keluar` int(11) NOT NULL,
  `no_plat` varchar(20) NOT NULL,
  `waktu` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `laporan_keluar`
--

INSERT INTO `laporan_keluar` (`id_keluar`, `no_plat`, `waktu`) VALUES
(1, 'G6876ANF', '2021-12-27 14:45:39'),
(2, 'G5690RE', '2021-12-27 14:45:43'),
(3, 'B4521RFS', '2021-12-27 14:45:49'),
(4, '5182 YJ', '2022-01-03 01:20:12'),
(5, '5182 YJ26', '2022-01-03 01:25:10'),
(6, 'G 5182 YJ', '2022-01-03 01:25:38');

-- --------------------------------------------------------

--
-- Table structure for table `laporan_masuk`
--

CREATE TABLE `laporan_masuk` (
  `id_masuk` int(11) NOT NULL,
  `no_plat` varchar(20) NOT NULL,
  `waktu` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `laporan_masuk`
--

INSERT INTO `laporan_masuk` (`id_masuk`, `no_plat`, `waktu`) VALUES
(5, 'G6876ANF', '2021-12-27 14:43:02'),
(6, 'G 5678 AF', '2021-12-15 04:10:53'),
(7, 'B4521RFS', '2021-12-27 14:44:08'),
(8, 'G5690RE', '2021-12-27 14:44:18'),
(16, '5182', '2022-01-03 01:22:02'),
(17, '5182 YJ', '2022-01-03 01:24:01'),
(18, '3907 Mo', '2022-01-03 03:57:40'),
(19, '4987', '2022-01-03 03:57:47'),
(20, '07 Nq42*22', '2022-01-03 03:58:17'),
(21, '987Kq4222', '2022-01-03 03:58:27'),
(22, '3987 Mo', '2022-01-03 03:58:39'),
(23, 'NQ|3987', '2022-01-03 03:58:44'),
(24, '3987 Mo2*24', '2022-01-03 03:58:48'),
(25, '3987 MQ', '2022-01-03 03:58:58'),
(26, '3987} NQ', '2022-01-03 03:59:31'),
(27, '3938 HG', '2022-01-03 04:50:43'),
(29, 'G2781MN', '2022-01-17 05:35:24');

-- --------------------------------------------------------

--
-- Stand-in structure for view `masuk`
-- (See below for the actual view)
--
CREATE TABLE `masuk` (
`nama` varchar(50)
,`no_plat` varchar(20)
,`waktu` timestamp
,`keterangan` varchar(20)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `rekap_laporan`
-- (See below for the actual view)
--
CREATE TABLE `rekap_laporan` (
`nama` varchar(50)
,`no_plat` varchar(20)
,`waktu_masuk` timestamp
,`waktu_keluar` timestamp
,`keterangan` varchar(20)
);

-- --------------------------------------------------------

--
-- Structure for view `keluar`
--
DROP TABLE IF EXISTS `keluar`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `keluar`  AS SELECT `karyawan`.`nama` AS `nama`, `laporan_keluar`.`no_plat` AS `no_plat`, `laporan_keluar`.`waktu` AS `waktu`, CASE WHEN `karyawan`.`plat_nomor` = `laporan_keluar`.`no_plat` THEN `karyawan`.`status` ELSE 'TAMU' END AS `keterangan` FROM (`laporan_keluar` left join `karyawan` on(`karyawan`.`plat_nomor` = `laporan_keluar`.`no_plat`)) WHERE `karyawan`.`plat_nomor` is null OR `karyawan`.`plat_nomor` = `laporan_keluar`.`no_plat` ;

-- --------------------------------------------------------

--
-- Structure for view `masuk`
--
DROP TABLE IF EXISTS `masuk`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `masuk`  AS SELECT `karyawan`.`nama` AS `nama`, `laporan_masuk`.`no_plat` AS `no_plat`, `laporan_masuk`.`waktu` AS `waktu`, CASE WHEN `karyawan`.`plat_nomor` = `laporan_masuk`.`no_plat` THEN `karyawan`.`status` ELSE 'TAMU' END AS `keterangan` FROM (`laporan_masuk` left join `karyawan` on(`karyawan`.`plat_nomor` = `laporan_masuk`.`no_plat`)) WHERE `karyawan`.`plat_nomor` is null OR `karyawan`.`plat_nomor` = `laporan_masuk`.`no_plat` ;

-- --------------------------------------------------------

--
-- Structure for view `rekap_laporan`
--
DROP TABLE IF EXISTS `rekap_laporan`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rekap_laporan`  AS SELECT `masuk`.`nama` AS `nama`, `masuk`.`no_plat` AS `no_plat`, `masuk`.`waktu` AS `waktu_masuk`, `keluar`.`waktu` AS `waktu_keluar`, `masuk`.`keterangan` AS `keterangan` FROM (`masuk` left join `keluar` on(`keluar`.`no_plat` = `masuk`.`no_plat`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indexes for table `hasil_scan`
--
ALTER TABLE `hasil_scan`
  ADD PRIMARY KEY (`id_scan`);

--
-- Indexes for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD PRIMARY KEY (`id_krywn`);

--
-- Indexes for table `laporan_keluar`
--
ALTER TABLE `laporan_keluar`
  ADD PRIMARY KEY (`id_keluar`),
  ADD UNIQUE KEY `id_keluar` (`id_keluar`);

--
-- Indexes for table `laporan_masuk`
--
ALTER TABLE `laporan_masuk`
  ADD PRIMARY KEY (`id_masuk`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `hasil_scan`
--
ALTER TABLE `hasil_scan`
  MODIFY `id_scan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `karyawan`
--
ALTER TABLE `karyawan`
  MODIFY `id_krywn` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `laporan_keluar`
--
ALTER TABLE `laporan_keluar`
  MODIFY `id_keluar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `laporan_masuk`
--
ALTER TABLE `laporan_masuk`
  MODIFY `id_masuk` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
