-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 20, 2024 at 07:33 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `securite_sociale`
--
CREATE DATABASE IF NOT EXISTS `securite_sociale` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `securite_sociale`;

-- --------------------------------------------------------

--
-- Table structure for table `demandes`
--

DROP TABLE IF EXISTS `demandes`;
CREATE TABLE `demandes` (
  `id` int(11) NOT NULL,
  `recev_id` int(11) NOT NULL,
  `envoi_id` int(11) NOT NULL,
  `datedemande` datetime NOT NULL,
  `confirmation` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `demandes`
--

INSERT INTO `demandes` (`id`, `recev_id`, `envoi_id`, `datedemande`, `confirmation`) VALUES
(304, 1, 19, '2024-08-20 12:04:46', 1),
(305, 18, 19, '2024-08-20 12:04:59', 0),
(306, 19, 19, '2024-08-20 12:05:07', 0),
(307, 18, 1, '2024-08-20 12:06:00', 0),
(308, 19, 1, '2024-08-20 12:06:09', 0),
(309, 1, 18, '2024-08-20 12:06:37', 0),
(310, 19, 18, '2024-08-20 12:06:47', 0),
(312, 1, 1, '2024-08-20 13:43:38', 0),
(313, 5, 1, '2024-08-20 13:43:43', 0),
(314, 6, 1, '2024-08-20 15:07:29', 0),
(315, 19, 1, '2024-08-20 16:05:05', 0),
(317, 18, 18, '2024-08-20 19:21:07', 0);

-- --------------------------------------------------------

--
-- Table structure for table `imgs`
--

DROP TABLE IF EXISTS `imgs`;
CREATE TABLE `imgs` (
  `id` int(11) NOT NULL,
  `image` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `imgs`
--

INSERT INTO `imgs` (`id`, `image`) VALUES
(13, 'e71668c4-22b1-4dd8-bbfa-507da9a764cf.jpeg'),
(14, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(15, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(16, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(17, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(18, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(19, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(20, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(21, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(22, '5c516333-07f6-4c2c-b8e2-8701b32e1212.jpeg'),
(23, '5c516333-07f6-4c2c-b8e2-8701b32e1212.jpeg'),
(24, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(25, 'ff8fd44e-e458-4a0d-a7cd-b16c2a8d7aa3.jpeg'),
(26, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(27, 'ed34308d-3fad-432d-8f41-1ec8c41e1a70.jpeg'),
(28, '8e9679c7-166d-4328-8bbf-239816fd58c4.jpeg'),
(29, 'c8409695-7c7f-4468-95b8-e60f31b42306.jpeg'),
(30, '47a134dd-5150-4540-9667-515cc21d54f7.jpeg'),
(31, '7b864c9f-285a-4ccd-8598-90557b5ba081.jpeg'),
(32, 'user.png'),
(33, 'téléchargement.png'),
(34, '1f0e6eb2-2815-4d2b-85d0-097205bafecd.png');

-- --------------------------------------------------------

--
-- Stand-in structure for view `listeami`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `listeami`;
CREATE TABLE `listeami` (
`iduser` int(11)
,`nom` varchar(50)
,`postnom` varchar(50)
,`prenom` varchar(50)
,`email` varchar(50)
,`avatar` text
,`telephone` varchar(20)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `listeamis`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `listeamis`;
CREATE TABLE `listeamis` (
`id` int(11)
,`nom` varchar(50)
,`postnom` varchar(50)
,`prenom` varchar(50)
,`password` text
,`email` varchar(50)
,`avatar` text
,`telephone` varchar(20)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `listedemandes`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `listedemandes`;
CREATE TABLE `listedemandes` (
`idc` int(11)
,`id` int(11)
,`nom` varchar(50)
,`postnom` varchar(50)
,`prenom` varchar(50)
,`email` varchar(50)
,`password` text
,`avatar` text
,`telephone` varchar(20)
,`recev_id` int(11)
,`datedemande` datetime
,`envoi_id` int(11)
,`confirmation` tinyint(1)
);

-- --------------------------------------------------------

--
-- Table structure for table `localisations`
--

DROP TABLE IF EXISTS `localisations`;
CREATE TABLE `localisations` (
  `id` int(11) NOT NULL,
  `iduser` int(11) NOT NULL,
  `longitude` float NOT NULL,
  `latitude` float NOT NULL,
  `datelocalisation` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mesnotification`
--

DROP TABLE IF EXISTS `mesnotification`;
CREATE TABLE `mesnotification` (
  `id` int(11) NOT NULL,
  `id_rec` int(11) NOT NULL,
  `id_sender` int(11) NOT NULL,
  `messages` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mesnotification`
--

INSERT INTO `mesnotification` (`id`, `id_rec`, `id_sender`, `messages`) VALUES
(1, 16, 1, 'gggg'),
(2, 16, 1, 'gggg'),
(3, 16, 1, 'gggg'),
(4, 16, 1, 'gggg'),
(5, 16, 1, 'gggg'),
(6, 16, 1, 'gggg'),
(7, 16, 1, 'gggg'),
(8, 16, 1, 'gggg'),
(9, 16, 1, 'gggg'),
(10, 16, 1, 'gggg'),
(11, 16, 1, 'gggg'),
(12, 16, 1, 'gggg'),
(13, 16, 1, 'gggg'),
(14, 16, 1, 'gggg'),
(15, 16, 1, 'gggg');

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
CREATE TABLE `notes` (
  `id` int(11) NOT NULL,
  `id_rec` int(11) NOT NULL,
  `messages` varchar(400) NOT NULL,
  `id_sender` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notes`
--

INSERT INTO `notes` (`id`, `id_rec`, `messages`, `id_sender`) VALUES
(2, 1, 'blabla', 16);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `recev_id` int(11) NOT NULL,
  `envoi_id` int(11) NOT NULL,
  `contenu` text NOT NULL,
  `datenotification` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `postnom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` text NOT NULL,
  `avatar` text NOT NULL,
  `telephone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nom`, `postnom`, `prenom`, `email`, `password`, `avatar`, `telephone`) VALUES
(1, 'Famba', 'Ngoy', 'Pierre', 'pierrpapy@gmail.com', '$2b$12$m5ofM/HN/3YKxkG505jYXuG0Df52q.RTzVWqi/WUh9304VFs.qgG2', 'user.png', '0898596591'),
(5, 'Kilangalanga', 'Ngayenge', 'Jean-Pierre', 'pierrepapy@gmail.com', '$2b$12$trZeVx4CNHtp8EgblRgYGOdtrEQnRxBRggwufPHfo/2EdiDhdNxVG', 'user.png', '0898560566788'),
(6, 'Ngoma', 'Kwesabio ', 'Moïse ', 'pierrepapys@gmail.com', '$2b$12$uQqwJDReE1HN75avyzy8te4S9nRKNlRst8/vC76XsWpwKbvPCuDly', 'user.png', '0898596501'),
(7, 'Bola', 'Lobota', 'Patrick ', 'bola@gmail.com', '$2b$12$QTYcgE/HpXW5spEJISHeCuXH/A2CaYexKHniGgo6Ycu.cNBO9BV/6', '3a21f4cb-271f-4863-b9de-42a950aaacf6.jpeg', '0818596501'),
(8, 'Basele', 'Wenge', 'Tigana', 'basele@gmail.com', '$2b$12$/ZVGwi6rVeZTfEJ1d44VQeDD2c08/lMRhTiDEwO.RyVoPnYbaCHUW', 'user.png', '08976435567'),
(9, 'Sindani', 'Sindani', 'Josiane', 'epiphani@gmail.com', '$2b$12$RXPw4f1uiCsBT9n3XBfI5uH1mVLxEupOehybWEvin3VidTkPb2aae', '29ca863a-bf2b-4ca8-8b00-b3e8e17eeb79.jpeg', '0812345687'),
(10, 'Kasereka ', 'Kalimumbalo', 'Eric', 'kalimumbalo@gmail.com', '$2b$12$2v34eBm.pXW8zO66EE4CV.A.beD6Xj3aYgyg179DLciSAU/R1X2Ki', 'user.png', '00034'),
(11, 'Mitongo', 'Kabeya', 'Renedis', 'mito@gmail.com', '$2b$12$47TQJvoIoyb4ZY1Tu2R/0.rzuHSC0jDDsXcZX1GJndApDlGfLFWyO', 'user.png', '057777'),
(12, 'Kibeti', 'Sulu', 'Dan', 'kibeti@gmail.com', '$2b$12$ne9Z2ZxsZqu89J25UAQg9eZWroLvOeY7RixzjAJEeanBTJ//n8QVy', 'user.png', '087654'),
(13, 'Ilongo', 'Tokombe', 'Jean', 'tokombe@gmail.com', '$2b$12$ItNFVe9Bg7cH0RbXc6BkIeKRtbXK0mVOQMzmCxVIb7D3.YGc0n/TO', 'user.png', '87655'),
(14, 'Jiji', 'Balue', 'Patrick ', 'jiji@gmail.com', '$2b$12$Mc0AhPfE5woy74sShjuE4OaCuiR0cOVOzJ0IVL86d/vWo4BmmK582', 'user.png', '8765555'),
(15, 'Kalume', 'Kamango', 'Papy', 'kamango@gmail.com', '$2b$12$JJGH/Px2W9m3bYvvlw1RSeyD2rmqfcaR1/mjdt71W2X4usjswwCCe', 'user.png', '677888'),
(16, 'Ngoy', 'Yambayamba', 'Papy', 'ngoy@gmail.com', '$2b$12$qw/MuotyTnsdQ7zW1vs1i.OGYjwebmvOTXEnbCkaOIYtNDcue/FDe', 'user.png', '786544'),
(17, 'Kambale', 'Kahongwa', 'Serge', 'kahingwa@gmail.com', '$2b$12$sd7FINRFY090qMwsRHXjVOo7QdhcR0Kf6G9qr.L/PREIIhxHU2MZe', 'a1d6ad7e-646c-4d9b-a812-deaeea91e77b.jpeg', '865438677'),
(18, 'Mulamba', 'Kibonge', 'Gédéon ', 'mulamba@gmail.com', '$2b$12$hehFX9FNyqUOGvl7cggilOCDVS8DL6sZbDV2awa037FwRyh7eE4VC', 'dbfc1084-d019-4bc7-85e9-1bdc5b23087c.jpeg', '876555556'),
(19, 'Nsevani', 'Kitonge', 'Manassé ', 'nsevani@gmail.com', '$2b$12$G2peGs5XuZwfFuTn.M0Hce6dk2nmDp.tJuvGcmpJEKHnDgGXbEaey', 'user.png', '567778');

-- --------------------------------------------------------

--
-- Table structure for table `validations`
--

DROP TABLE IF EXISTS `validations`;
CREATE TABLE `validations` (
  `id` int(11) NOT NULL,
  `iduser` int(11) NOT NULL,
  `datevalidation` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure for view `listeami`
--
DROP TABLE IF EXISTS `listeami`;

DROP VIEW IF EXISTS `listeami`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `listeami`  AS SELECT `users`.`id` AS `iduser`, `users`.`nom` AS `nom`, `users`.`postnom` AS `postnom`, `users`.`prenom` AS `prenom`, `users`.`email` AS `email`, `users`.`avatar` AS `avatar`, `users`.`telephone` AS `telephone` FROM (`users` left join `demandes` on(`users`.`id` = `demandes`.`envoi_id`)) WHERE `demandes`.`envoi_id` is null ;

-- --------------------------------------------------------

--
-- Structure for view `listeamis`
--
DROP TABLE IF EXISTS `listeamis`;

DROP VIEW IF EXISTS `listeamis`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `listeamis`  AS SELECT `users`.`id` AS `id`, `users`.`nom` AS `nom`, `users`.`postnom` AS `postnom`, `users`.`prenom` AS `prenom`, `users`.`password` AS `password`, `users`.`email` AS `email`, `users`.`avatar` AS `avatar`, `users`.`telephone` AS `telephone` FROM `users` WHERE !(`users`.`id` in (select `demandes`.`recev_id` from `demandes` where `demandes`.`envoi_id` = '1')) ;

-- --------------------------------------------------------

--
-- Structure for view `listedemandes`
--
DROP TABLE IF EXISTS `listedemandes`;

DROP VIEW IF EXISTS `listedemandes`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `listedemandes`  AS SELECT `demandes`.`id` AS `idc`, `users`.`id` AS `id`, `users`.`nom` AS `nom`, `users`.`postnom` AS `postnom`, `users`.`prenom` AS `prenom`, `users`.`email` AS `email`, `users`.`password` AS `password`, `users`.`avatar` AS `avatar`, `users`.`telephone` AS `telephone`, `demandes`.`recev_id` AS `recev_id`, `demandes`.`datedemande` AS `datedemande`, `demandes`.`envoi_id` AS `envoi_id`, `demandes`.`confirmation` AS `confirmation` FROM (`demandes` join `users`) WHERE `users`.`id` = `demandes`.`envoi_id` AND `demandes`.`confirmation` = '0' ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `demandes`
--
ALTER TABLE `demandes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `imgs`
--
ALTER TABLE `imgs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `localisations`
--
ALTER TABLE `localisations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mesnotification`
--
ALTER TABLE `mesnotification`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `validations`
--
ALTER TABLE `validations`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `demandes`
--
ALTER TABLE `demandes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=318;

--
-- AUTO_INCREMENT for table `imgs`
--
ALTER TABLE `imgs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `localisations`
--
ALTER TABLE `localisations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mesnotification`
--
ALTER TABLE `mesnotification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `notes`
--
ALTER TABLE `notes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `validations`
--
ALTER TABLE `validations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
