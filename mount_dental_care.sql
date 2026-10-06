-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 21, 2026 at 01:09 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mount_dental_care`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Site Settings', 7, 'add_sitesettings'),
(26, 'Can change Site Settings', 7, 'change_sitesettings'),
(27, 'Can delete Site Settings', 7, 'delete_sitesettings'),
(28, 'Can view Site Settings', 7, 'view_sitesettings'),
(29, 'Can add nav item', 8, 'add_navitem'),
(30, 'Can change nav item', 8, 'change_navitem'),
(31, 'Can delete nav item', 8, 'delete_navitem'),
(32, 'Can view nav item', 8, 'view_navitem'),
(33, 'Can add offer banner', 9, 'add_offerbanner'),
(34, 'Can change offer banner', 9, 'change_offerbanner'),
(35, 'Can delete offer banner', 9, 'delete_offerbanner'),
(36, 'Can view offer banner', 9, 'view_offerbanner'),
(37, 'Can add service', 10, 'add_service'),
(38, 'Can change service', 10, 'change_service'),
(39, 'Can delete service', 10, 'delete_service'),
(40, 'Can view service', 10, 'view_service'),
(41, 'Can add trust feature', 11, 'add_trustfeature'),
(42, 'Can change trust feature', 11, 'change_trustfeature'),
(43, 'Can delete trust feature', 11, 'delete_trustfeature'),
(44, 'Can view trust feature', 11, 'view_trustfeature'),
(45, 'Can add doctor', 12, 'add_doctor'),
(46, 'Can change doctor', 12, 'change_doctor'),
(47, 'Can delete doctor', 12, 'delete_doctor'),
(48, 'Can view doctor', 12, 'view_doctor'),
(49, 'Can add gallery item', 13, 'add_galleryitem'),
(50, 'Can change gallery item', 13, 'change_galleryitem'),
(51, 'Can delete gallery item', 13, 'delete_galleryitem'),
(52, 'Can view gallery item', 13, 'view_galleryitem'),
(53, 'Can add clinic address', 14, 'add_clinicaddress'),
(54, 'Can change clinic address', 14, 'change_clinicaddress'),
(55, 'Can delete clinic address', 14, 'delete_clinicaddress'),
(56, 'Can view clinic address', 14, 'view_clinicaddress'),
(57, 'Can add clinic hour', 15, 'add_clinichour'),
(58, 'Can change clinic hour', 15, 'change_clinichour'),
(59, 'Can delete clinic hour', 15, 'delete_clinichour'),
(60, 'Can view clinic hour', 15, 'view_clinichour'),
(61, 'Can add footer link', 16, 'add_footerlink'),
(62, 'Can change footer link', 16, 'change_footerlink'),
(63, 'Can delete footer link', 16, 'delete_footerlink'),
(64, 'Can view footer link', 16, 'view_footerlink'),
(65, 'Can add page content', 17, 'add_pagecontent'),
(66, 'Can change page content', 17, 'change_pagecontent'),
(67, 'Can delete page content', 17, 'delete_pagecontent'),
(68, 'Can view page content', 17, 'view_pagecontent'),
(69, 'Can add Email Template', 18, 'add_emailtemplate'),
(70, 'Can change Email Template', 18, 'change_emailtemplate'),
(71, 'Can delete Email Template', 18, 'delete_emailtemplate'),
(72, 'Can view Email Template', 18, 'view_emailtemplate'),
(73, 'Can add appointment', 19, 'add_appointment'),
(74, 'Can change appointment', 19, 'change_appointment'),
(75, 'Can delete appointment', 19, 'delete_appointment'),
(76, 'Can view appointment', 19, 'view_appointment'),
(77, 'Can add notification', 20, 'add_notification'),
(78, 'Can change notification', 20, 'change_notification'),
(79, 'Can delete notification', 20, 'delete_notification'),
(80, 'Can view notification', 20, 'view_notification'),
(81, 'Can add email otp', 21, 'add_emailotp'),
(82, 'Can change email otp', 21, 'change_emailotp'),
(83, 'Can delete email otp', 21, 'delete_emailotp'),
(84, 'Can view email otp', 21, 'view_emailotp'),
(85, 'Can add Hero Banner', 22, 'add_herobanner'),
(86, 'Can change Hero Banner', 22, 'change_herobanner'),
(87, 'Can delete Hero Banner', 22, 'delete_herobanner'),
(88, 'Can view Hero Banner', 22, 'view_herobanner'),
(89, 'Can add Email log', 23, 'add_emaillog'),
(90, 'Can change Email log', 23, 'change_emaillog'),
(91, 'Can delete Email log', 23, 'delete_emaillog'),
(92, 'Can view Email log', 23, 'view_emaillog'),
(93, 'Can add Award', 24, 'add_award'),
(94, 'Can change Award', 24, 'change_award'),
(95, 'Can delete Award', 24, 'delete_award'),
(96, 'Can view Award', 24, 'view_award'),
(97, 'Can add Branch', 25, 'add_branch'),
(98, 'Can change Branch', 25, 'change_branch'),
(99, 'Can delete Branch', 25, 'delete_branch'),
(100, 'Can view Branch', 25, 'view_branch'),
(101, 'Can add Clinic tour image', 26, 'add_clinicimage'),
(102, 'Can change Clinic tour image', 26, 'change_clinicimage'),
(103, 'Can delete Clinic tour image', 26, 'delete_clinicimage'),
(104, 'Can view Clinic tour image', 26, 'view_clinicimage'),
(105, 'Can add Text block', 27, 'add_sitetext'),
(106, 'Can change Text block', 27, 'change_sitetext'),
(107, 'Can delete Text block', 27, 'delete_sitetext'),
(108, 'Can view Text block', 27, 'view_sitetext'),
(109, 'Can add YouTube video', 28, 'add_youtubevideo'),
(110, 'Can change YouTube video', 28, 'change_youtubevideo'),
(111, 'Can delete YouTube video', 28, 'delete_youtubevideo'),
(112, 'Can view YouTube video', 28, 'view_youtubevideo');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clinic_appointment`
--

CREATE TABLE `clinic_appointment` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `mobile_number` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `preferred_date` date NOT NULL,
  `treatment_type` varchar(150) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `admin_note` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clinic_award`
--

CREATE TABLE `clinic_award` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `category` varchar(150) NOT NULL,
  `description` longtext NOT NULL,
  `venue` varchar(200) NOT NULL,
  `event_date` varchar(120) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_award`
--

INSERT INTO `clinic_award` (`id`, `title`, `category`, `description`, `venue`, `event_date`, `image`, `sort_order`, `active`) VALUES
(1, 'Best Paper Presentation Award', 'Forensic Odontology', 'Dr. S. Natesh received the Best paper presentation award in Forensic Odontology from Padma Bhushan Brig. Anil Kohli, President, Dental Council of India on 20th January 2008 held in Dr. M.G.R. University, Chennai.', 'Dr. M.G.R. University, Chennai', '20th January 2008', 'awards/award_mgr_university.jpg', 0, 1),
(2, 'Best Paper Presentation Award', 'Innovative Teaching Methods', 'Dr. S. Natesh won the Best paper presentation Award on \"FORMATIVE ASSESSMENT OF INNOVATIVE TEACHING METHODS\" in APTCON08 on 13th July 08 held in Sri Ramachandra University, Chennai.', 'Sri Ramachandra University, Chennai', '13th July 2008', 'awards/award_srmc_university.jpg', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_branch`
--

CREATE TABLE `clinic_branch` (
  `id` bigint(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `phone_display` varchar(80) NOT NULL,
  `phone_dial` varchar(30) NOT NULL,
  `address` longtext NOT NULL,
  `map_embed_url` varchar(600) NOT NULL,
  `map_directions_url` varchar(600) NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_branch`
--

INSERT INTO `clinic_branch` (`id`, `name`, `phone_display`, `phone_dial`, `address`, `map_embed_url`, `map_directions_url`, `is_primary`, `sort_order`, `active`) VALUES
(1, 'St. Thomas Mount Branch', '044-2234 5000', '04422345000', '5/66-1A, Butt Rd, St. Thomas Mount, Chennai - 600016', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3887.987843210000!2d80.17000000000000!3d13.01000000000000!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a52674853a74b83%3A0x2181e234367e053f!2sMount%20Multispeciality%20Dental%20Clinic!5e0!3m2!1sen!2sin!4v1600000000000', 'https://www.google.com/maps/place/Mount+Multispeciality+Dental+Clinic+St.Thomas+Mount,+Mount+Multispeciality+Dental+Clinic,+5%2F66-1A,+Butt+Rd,+Ramapuram,+Parangi+Malai,+St.Thomas+Mount,+Chennai,+Tamil+Nadu+600016/data=!4m2!3m1!1s0x3a52674853a74b83:0x2181e234367e053f!18m1!1e1', 1, 0, 1),
(2, 'Nungambakkam Branch', '044-2827 5000', '04428275000', '37/2, Jambulingam St, Nungambakkam, Chennai - 600034', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3886.000000000000!2d80.24000000000000!3d13.06000000000000!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a526667f0d45565%3A0xcc5423acd0f5aee9!2sMount%20Multispeciality%20Dental%20Clinic%20Nungambakkam!5e0!3m2!1sen!2sin!4v1600000000001', 'https://www.google.com/maps/place/Mount+Multispeciality+Dental+Clinic+Nungambakkam,+37%2F2,+Jambulingam+street,+Facing,+Valluvar+Kottam+High+Rd,+Nungambakkam,+Chennai,+Tamil+Nadu+600034/data=!4m2!3m1!1s0x3a526667f0d45565:0xcc5423acd0f5aee9!18m1!1e1', 0, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_clinicaddress`
--

CREATE TABLE `clinic_clinicaddress` (
  `id` bigint(20) NOT NULL,
  `label` varchar(80) NOT NULL,
  `address` longtext NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_clinicaddress`
--

INSERT INTO `clinic_clinicaddress` (`id`, `label`, `address`, `sort_order`, `active`) VALUES
(1, 'Clinic Location', '5/66–1A, Butt Road, St. Thomas Mount, Chennai 600016', 0, 1),
(2, 'Clinic Location', '37/2, 1st Floor, Valluvar Kottam High Road, Nungambakkam, Chennai 600034', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_clinichour`
--

CREATE TABLE `clinic_clinichour` (
  `id` bigint(20) NOT NULL,
  `day` varchar(50) NOT NULL,
  `hours` varchar(100) NOT NULL,
  `emergency` tinyint(1) NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_clinichour`
--

INSERT INTO `clinic_clinichour` (`id`, `day`, `hours`, `emergency`, `sort_order`) VALUES
(1, 'Mon - Sat', 'Morning - 10.00 AM - 01.00 PM | Evening 05.00 PM - 08.30 PM', 0, 0),
(2, 'St.Thomas Mount - 044-2234 5000', 'Nungambakkam - 044-2827 5000', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_clinicimage`
--

CREATE TABLE `clinic_clinicimage` (
  `id` bigint(20) NOT NULL,
  `title` varchar(150) NOT NULL,
  `caption` varchar(200) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_clinicimage`
--

INSERT INTO `clinic_clinicimage` (`id`, `title`, `caption`, `image`, `sort_order`, `active`) VALUES
(1, 'Modern Operatory Suites', 'Designed for sterile comfort and advanced patient care', 'hero-banners/dental-clinic.jpg', 0, 1),
(2, 'High-Tech Treatment Stations', 'Ergonomic dental units with integrated digital controls', 'hero-banners/clinic-equipment.jpeg', 1, 1),
(3, '3D CBCT Diagnostic Scanning', 'Ultra-low dose volumetric imaging for precision planning', 'hero-banners/cbct-scan.jpeg', 2, 1),
(4, 'Clinical Excellence & Sterilization', 'Hospital-grade multi-stage autoclave hygiene standards', 'site/why-dental.jpg', 3, 1),
(5, 'Digital Intraoral Imaging', 'High-magnification intraoral cameras for accurate assessment', 'site/why-technology.jpg', 4, 1),
(6, 'Inside Our Clinic', 'A comfortable, modern space designed around patients', 'clinic/sample-3.jpg', 5, 1),
(7, 'Patient Care Suite', 'Precision treatment delivered with a gentle touch', 'clinic/sample-4.jpg', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_doctor`
--

CREATE TABLE `clinic_doctor` (
  `id` bigint(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `role` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `bio` longtext NOT NULL,
  `education` varchar(255) NOT NULL,
  `expertise` varchar(255) NOT NULL,
  `tenure` varchar(255) NOT NULL,
  `memberships` varchar(255) NOT NULL,
  `is_lead` tinyint(1) NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_doctor`
--

INSERT INTO `clinic_doctor` (`id`, `name`, `role`, `image`, `bio`, `education`, `expertise`, `tenure`, `memberships`, `is_lead`, `sort_order`, `active`) VALUES
(1, 'Dr. S. NATESH M.D.S.', 'Lead Dentist & Founder • Consultant Dental Surgeon, Endodontist & Implantologist • 21+ Years Experience', 'doctors/natesh.jpg', 'Dr. S. Natesh is a Consultant Dental Surgeon, Endodontist and Implantologist with 21+ years of clinical experience. He has extensive experience in endodontic care, implantology, veneers and digital smile design, including more than 3,000 dental implant placements.', 'BDS, MDS', 'Implantology, Veneers, Digital Smile Design', '21+ Years Active Clinical Practice', 'Indian Dental Association (IDA)', 1, 0, 1),
(2, 'Dr. N. PADMINI M.D.S.', 'Consultant Dental Surgeon & Orthodontist', 'doctors/padmini.jpg', '', '', '', '', '', 0, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_emaillog`
--

CREATE TABLE `clinic_emaillog` (
  `id` bigint(20) NOT NULL,
  `template_type` varchar(40) NOT NULL,
  `recipient` varchar(254) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `status` varchar(10) NOT NULL,
  `error` longtext NOT NULL,
  `attempts` smallint(5) UNSIGNED NOT NULL CHECK (`attempts` >= 0),
  `created_at` datetime(6) NOT NULL,
  `last_attempt_at` datetime(6) NOT NULL,
  `appointment_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clinic_emailotp`
--

CREATE TABLE `clinic_emailotp` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `mobile_number` varchar(50) NOT NULL,
  `preferred_date` date NOT NULL,
  `treatment_type` varchar(150) NOT NULL,
  `message` longtext NOT NULL,
  `otp_hash` varchar(128) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `attempts` smallint(5) UNSIGNED NOT NULL CHECK (`attempts` >= 0),
  `verified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clinic_emailtemplate`
--

CREATE TABLE `clinic_emailtemplate` (
  `id` bigint(20) NOT NULL,
  `template_type` varchar(60) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `active` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_emailtemplate`
--

INSERT INTO `clinic_emailtemplate` (`id`, `template_type`, `subject`, `body`, `active`, `updated_at`) VALUES
(1, 'appointment_otp', 'Your Mount Dental Care verification code is {{otp}}', 'Hello {{full_name}},\n\nYour Mount Dental Care appointment verification code is: {{otp}}\n\nThis code expires in {{expiry_minutes}} minutes. Do not share this code with anyone.\n\nAppointment date: {{preferred_date}}\nTreatment: {{treatment_type}}\n\nMount Dental Care', 1, '2026-09-21 11:04:12.125954'),
(5, 'admin_appointment_notify', 'New Appointment Booking - {{full_name}} ({{treatment_type}})', 'A new appointment has been booked on Mount Dental Care.\n\n--- Patient Details ---\nName: {{full_name}}\nMobile: {{mobile_number}}\nEmail: {{email}}\nPreferred Date: {{preferred_date}}\nTreatment: {{treatment_type}}\nMessage: {{message}}\n\nBooked at: {{booked_at}}\nAppointment ID: {{appointment_id}}\n\nPlease log in to the admin panel to review and confirm this appointment.\n\n-- Mount Dental Care System', 1, '2026-09-21 11:04:13.290330');

-- --------------------------------------------------------

--
-- Table structure for table `clinic_footerlink`
--

CREATE TABLE `clinic_footerlink` (
  `id` bigint(20) NOT NULL,
  `group` varchar(80) NOT NULL,
  `label` varchar(150) NOT NULL,
  `url` varchar(255) NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_footerlink`
--

INSERT INTO `clinic_footerlink` (`id`, `group`, `label`, `url`, `sort_order`, `active`) VALUES
(1, 'quick', 'About Our Clinic', '#about-clinic', 0, 1),
(2, 'quick', 'Our Doctors & Team', '#our-dentists', 1, 1),
(3, 'quick', 'Smile Gallery & Results', '#smile-gallery', 2, 1),
(4, 'quick', 'Why Choose Us', '#why-choose-us', 3, 1),
(5, 'quick', 'Awards & Recognitions', '#awards', 4, 1),
(6, 'treatments', 'Laser Teeth Whitening', '#services', 0, 1),
(7, 'treatments', 'Dental Implants (Titanium & Zirconia)', '#services', 1, 1),
(8, 'treatments', 'Clear Aligners & Braces', '#services', 2, 1),
(9, 'treatments', 'Comfortable Root Canal Treatment', '#services', 3, 1),
(10, 'treatments', 'Porcelain Cosmetic Veneers', '#services', 4, 1),
(11, 'treatments', 'Children’s Pediatric Care', '#services', 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_galleryitem`
--

CREATE TABLE `clinic_galleryitem` (
  `id` bigint(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `video` varchar(100) DEFAULT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_galleryitem`
--

INSERT INTO `clinic_galleryitem` (`id`, `title`, `description`, `image`, `video`, `sort_order`, `active`) VALUES
(1, 'INTERVIEW', 'Interview of Dr. S. Natesh on SUN NEWS Satellite Television for DOCTOR\'S NEWS on 9-9-2010 from 11AM to 12 NOON Live Programme.', 'gallery/interview-natesh-sun-news-2010.jpg', '', 0, 1),
(2, 'INTERVIEW', 'Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television in \"Doctor Sun News\" Program held on March 2007 between 8:00pm - 9:00 pm.', 'gallery/interview-subhashini-doctor-sun-news-2007.jpg', '', 1, 1),
(3, 'INTERVIEW', 'Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television for DOCTOR\'S NEWS on 23.7.2010 from 11AM to 12 NOON Live Programme.', 'gallery/interview-subhashini-sun-news-2010.jpg', '', 2, 1),
(4, 'INTERVIEW', 'Interview of Dr. Natesh on Makkal TV in Maruthuva Neram held on, 18-11-2009 between 3:00pm - 4:00pm.', 'gallery/interview-sun-news.jpg', '', 3, 1),
(5, 'INTERVIEW', 'Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television in \"Doctor Sun News\" Program held on March 2008 between 8:00pm - 9:00 pm.', 'gallery/interview-subhashini-doctor-sun-news-2008.jpg', '', 4, 1),
(6, 'SUN NEWS INTERVIEW', 'Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television for \"Doctor Sun News\" Programme held on March 2008 between 8:00pm - 9:00 pm.', 'gallery/interview-natesh-makkal-tv-2009.jpg', '', 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_herobanner`
--

CREATE TABLE `clinic_herobanner` (
  `id` bigint(20) NOT NULL,
  `title` varchar(150) NOT NULL,
  `media_type` varchar(10) NOT NULL,
  `media` varchar(100) NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_herobanner`
--

INSERT INTO `clinic_herobanner` (`id`, `title`, `media_type`, `media`, `sort_order`, `active`) VALUES
(1, 'Advanced Dental Technology', 'image', 'hero-banners/clinic-equipment.jpeg', 0, 1),
(2, '3D CBCT Diagnostic Imaging', 'image', 'hero-banners/cbct-scan.jpeg', 1, 1),
(3, 'Modern Dental Clinic', 'image', 'hero-banners/dental-clinic.jpg', 2, 1),
(4, 'Clinic Tour', 'video', 'hero-banners/clinic-tour.mp4', 3, 1),
(5, 'Dental Technology Tour', 'video', 'hero-banners/technology-tour.mp4', 4, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_navitem`
--

CREATE TABLE `clinic_navitem` (
  `id` bigint(20) NOT NULL,
  `label` varchar(80) NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_navitem`
--

INSERT INTO `clinic_navitem` (`id`, `label`, `sort_order`, `active`) VALUES
(1, 'Home', 0, 1),
(2, 'Why Choose Us', 1, 1),
(3, 'Our Dentists', 2, 1),
(4, 'About Clinic', 3, 1),
(5, 'Smile Gallery', 4, 1),
(6, 'Awards', 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_notification`
--

CREATE TABLE `clinic_notification` (
  `id` bigint(20) NOT NULL,
  `title` varchar(160) NOT NULL,
  `message` longtext NOT NULL,
  `notification_type` varchar(30) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `appointment_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `email` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clinic_offerbanner`
--

CREATE TABLE `clinic_offerbanner` (
  `id` bigint(20) NOT NULL,
  `eyebrow` varchar(100) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `button_text` varchar(100) NOT NULL,
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_offerbanner`
--

INSERT INTO `clinic_offerbanner` (`id`, `eyebrow`, `title`, `description`, `button_text`, `active`) VALUES
(1, 'ADVANCED DENTAL DIAGNOSTICS', '3D CBCT Scan, Digital X-Ray & Intraoral Scan', 'Get a complete picture of your oral health with our state-of-the-art diagnostic package. Our 3D CBCT Scan delivers high-precision volumetric imaging for implant planning and complex treatments, Digital X-Rays provide instant low-radiation tooth and bone assessment, and our Intraoral Camera Scan captures detailed images inside your mouth for accurate, comfortable diagnosis — all in one visit at Mount Dental Care, Chennai.', 'Book Today', 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_pagecontent`
--

CREATE TABLE `clinic_pagecontent` (
  `id` bigint(20) NOT NULL,
  `key` varchar(80) NOT NULL,
  `eyebrow` varchar(150) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_pagecontent`
--

INSERT INTO `clinic_pagecontent` (`id`, `key`, `eyebrow`, `title`, `description`, `active`) VALUES
(1, 'why', 'THE MOUNT DENTAL DIFFERENCE', 'Why Patients Trust Mount Dental Care', 'We believe visiting the dentist should be pleasant, relaxed and genuinely reassuring. Our patient-first approach combines experienced specialists, advanced technology and compassionate care to create an experience patients can trust.', 1),
(2, 'about', 'ABOUT MOUNT DENTAL CARE', 'Setting the Standard for Compassionate, Modern Dentistry', 'Founded with a passion to redefine dental anxiety into a soothing, empowering health journey, Mount Dental Care has grown into a trusted dental clinic in Chennai, providing comprehensive dental care for individuals and families. We combine modern dental technology, clinical expertise and a patient-first approach to provide comfortable, personalized care.', 1),
(3, 'experts', 'MEET OUR EXPERTS', 'Led by Renowned Dental Specialists', 'Our clinicians regularly train in Switzerland and the US in the latest micro-surgical and aesthetic protocols.', 1),
(4, 'gallery', 'VISUAL TOUR & RESULTS', 'Our Smile Gallery & Clinic Experience', 'Explore our sterile, welcoming clinic suites, real patient transformations and state-of-the-art facilities.', 1),
(5, 'appointment', 'EASY ONLINE BOOKING', 'Schedule Your Smile Consultation', 'Take the first step towards better oral health. Select your preferred date and treatment, and our patient coordinator will confirm your dental appointment within 15 minutes.', 1),
(6, 'contact', 'GET IN TOUCH', 'We’d Love to Welcome You', 'Conveniently located with dedicated patient parking, accessible transit links and friendly reception support for a comfortable visit.', 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_service`
--

CREATE TABLE `clinic_service` (
  `id` bigint(20) NOT NULL,
  `icon` varchar(40) NOT NULL,
  `title` varchar(150) NOT NULL,
  `description` longtext NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL,
  `badge` varchar(150) NOT NULL,
  `full_description` longtext NOT NULL,
  `highlights` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_service`
--

INSERT INTO `clinic_service` (`id`, `icon`, `title`, `description`, `sort_order`, `active`, `badge`, `full_description`, `highlights`) VALUES
(1, 'stethoscope', 'General Dentistry', 'Comprehensive oral exams, digital X-rays, cavity diagnostics, preventive care and routine dental check-ups for the whole family — the everyday foundation of quality family dentistry.', 0, 1, 'PREVENTIVE & DIAGNOSTIC CARE', 'General dentistry forms the foundation of lifelong oral wellness for every member of your family. Our comprehensive consultations combine gentle physical exams, high-resolution digital intraoral cameras, and low-radiation digital radiography to detect early signs of decay, gum inflammation, and enamel wear long before they develop into complex dental issues.', 'Digital oral health evaluation and computerized cavity detection\nLow-radiation digital radiography & intraoral photo documentation\nBiocompatible tooth-colored composite restorations (aesthetic fillings)\nPreventive fluoride enamel applications & diagnostic bite analysis\nCustomized home oral hygiene roadmap and dietary guidance'),
(2, 'sparkles', 'Teeth Cleaning & Polishing', 'Gentle ultrasonic scaling and teeth cleaning to remove stubborn plaque and tartar buildup, helping keep your gums healthy and your smile fresh.', 1, 1, 'HYGIENE & GUM WELLNESS', 'Professional dental prophylaxis is essential for removing stubborn bacterial plaque and calcified tartar deposits that regular brushing cannot reach. Our clinicians utilize state-of-the-art ultrasonic scalers with fine micro-water sprays to gently dislodge calculus from tooth surfaces and below the gumline, followed by diamond-paste polishing that restores silky-smooth enamel luster.', 'Advanced gentle ultrasonic scaling to eliminate calculus and plaque\nSubgingival cleaning to prevent gingivitis and periodontal disease\nEnamel polishing with specialized prophy paste for stain removal\nRemoval of stubborn coffee, tea, and food surface discolorations\nAntiseptic gum soothing treatment for refreshed, healthy gums'),
(3, 'sun', 'Teeth Whitening', 'Advanced laser teeth whitening for a brighter, more confident smile. Our professional in-office treatment is designed to deliver noticeable results in a comfortable 45-minute visit.', 2, 1, 'AESTHETIC ENAMEL BRIGHTENING', 'Restore natural luminosity to your smile with our professional in-office laser teeth whitening system. Unlike abrasive over-the-counter kits, our clinical procedure uses a pH-balanced whitening formulation activated by targeted cool-light laser technology. This lifts deep enamel and dentin stains while strictly shielding your gums and maintaining tooth comfort.', 'Up to 6 to 8 shades lighter in a single, relaxed clinical session\nProtective light-cured gingival barrier to safeguard delicate gums\nControlled cool LED laser activation for optimal oxidation and stain breakdown\nSpecialized post-whitening potassium nitrate desensitizing treatment\nLong-lasting, radiant results with comprehensive aftercare instructions'),
(4, 'activity', 'Root Canal Treatment', 'Microscope-assisted, comfortable root canal treatment performed by our in-house endodontist to help save natural teeth and restore comfortable function.', 3, 1, 'MICROSCOPE-ASSISTED ENDODONTICS', 'When deep decay, cracks, or trauma reach the tooth\'s innermost nerve chamber, modern endodontic therapy saves the natural tooth and relieves acute discomfort. Utilizing high-magnification dental operating microscopes and computerized digital apex locators, our specialist cleans, disinfects, and hermetically seals the root canal anatomy with biocompatible gutta-percha, allowing you to chew with comfort and confidence.', 'Computer-guided local anesthesia for a genuinely comfortable experience\nMicroscope-assisted precision visualization of micro-canal branches\nFlexible nickel-titanium rotary file instrumentation for thorough cleaning\nBiocompatible hermetic seal to prevent reinfection and promote healing\nCustom crown preparation to restore structural strength and natural aesthetics'),
(5, 'shield', 'Dental Implants', 'Restore missing teeth with titanium and zirconia dental implants designed for natural function, comfort and a confident smile. Options include single implants, All-on-4 and full-mouth implants.', 4, 1, 'PERMANENT TOOTH RESTORATION', 'Dental implants represent the modern gold standard for replacing missing teeth. An implant consists of a medical-grade titanium or zirconia post that integrates directly with the alveolar bone, mimicking a natural tooth root. Topped with a custom handcrafted ceramic crown, implants prevent bone loss, restore 100% bite functionality, and blend seamlessly with your surrounding natural teeth.', '3D CBCT volumetric bone scan and virtual computer-guided planning\nBiocompatible titanium or metal-free ceramic zirconia implant fixtures\nPreserves natural jawbone density and youthful facial contours\nNo alteration or shaving down of adjacent healthy teeth required\nVersatile solutions from single tooth replacement to full-arch restorations'),
(6, 'layers', 'Braces & Clear Aligners', 'Personalized clear aligners, invisible aligners and discreet ceramic braces to straighten teeth, improve bite alignment and create a healthier, more confident smile for children, teens and adults.', 5, 1, 'DIGITAL ORTHODONTIC CORRECTION', 'Straighten your teeth and improve your bite with our advanced orthodontic treatment options. We provide custom invisible clear aligners that can be removed for eating and brushing, as well as discreet tooth-colored ceramic brackets. Every smile design journey starts with a 3D digital intraoral scan that projects your teeth\'s movement week by week until reaching your ideal smile.', 'Zero-impression 3D digital intraoral scanning with instant simulation\nRemovable, custom-molded invisible clear aligners for maximum convenience\nLow-profile aesthetic ceramic and self-ligating bracket options\nCorrection of crowding, gaps, overlapping teeth, overbites, and crossbites\nCustom post-treatment retainers to ensure your results last a lifetime'),
(7, 'smile', 'Cosmetic Dentistry', 'Transform your smile with custom porcelain veneers, composite resin veneers, aesthetic dental bonding and gummy smile contouring for natural-looking results.', 6, 1, 'CUSTOM SMILE MAKEOVERS', 'Cosmetic dentistry harmonizes science and artistic vision to create balanced, dazzling smiles. Whether you wish to repair minor chips with direct composite bonding, close gaps with ultra-thin porcelain veneers, or reshape an uneven gumline, our cosmetic clinicians craft each detail to complement your unique facial features, lip dynamics, and complexion.', 'Digital Smile Design (DSD) preview before any treatment begins\nUltra-thin handcrafted porcelain veneers with lifelike light translucency\nMinimally invasive composite resin bonding for chipped or uneven edges\nGentle aesthetic gum recontouring for balanced tooth-to-gum proportions\nFull smile transformations tailored for natural, long-lasting beauty'),
(8, 'baby', 'Children\'s Dentistry', 'Gentle, child-friendly pediatric dental care including dental check-ups, fluoride treatments and sealants for growing smiles.', 7, 1, 'GENTLE PEDIATRIC CARE', 'Creating a positive, trusting relationship with dental care during childhood sets the stage for a lifetime of healthy smiles. Our pediatric approach is tailored to make young patients feel secure and cheerful. From gentle cleanings and cavity-fighting mineral treatments to protective fissure sealants, we safeguard developing teeth while making every visit fun and relaxing.', 'Warm, engaging environment designed to eliminate pediatric dental apprehension\nGentle check-ups, tooth growth monitoring, and early bite tracking\nCavity-preventing fluoride varnish and protective tooth sealants\nGentle pediatric restorations with child-friendly terminology\nInteractive tooth-brushing instruction and nutritional guidance for parents');

-- --------------------------------------------------------

--
-- Table structure for table `clinic_sitesettings`
--

CREATE TABLE `clinic_sitesettings` (
  `id` bigint(20) NOT NULL,
  `clinic_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `hero_background_image` varchar(100) DEFAULT NULL,
  `hero_title` varchar(255) NOT NULL,
  `hero_description` longtext NOT NULL,
  `metric_dentists` varchar(80) NOT NULL,
  `metric_equipment` varchar(80) NOT NULL,
  `metric_emi` varchar(80) NOT NULL,
  `metric_patients` varchar(80) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `footer_about` longtext NOT NULL,
  `footer_copyright` varchar(200) NOT NULL,
  `topbar_hours` varchar(200) NOT NULL,
  `whatsapp_number` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_sitesettings`
--

INSERT INTO `clinic_sitesettings` (`id`, `clinic_name`, `email`, `logo`, `hero_background_image`, `hero_title`, `hero_description`, `metric_dentists`, `metric_equipment`, `metric_emi`, `metric_patients`, `updated_at`, `footer_about`, `footer_copyright`, `topbar_hours`, `whatsapp_number`) VALUES
(1, 'Mount Dental Care', 'mountdentalcare@gmail.com', 'site/logo.png', 'site/hero-background.jpg', 'Healthy Smiles, Lifelong Confidence', 'Looking for a dentist near me? Mount Dental Care is a trusted dental clinic in Chennai providing expert dental care and dental services with advanced technology and personalized treatment. From preventive care to dental implants, teeth whitening, braces and more, we provide compassionate care for the whole family, with same-day dental appointment slots available.', '15+', '3D CBCT', '0% EMI', '5,000+', '2026-09-21 11:04:21.624443', 'Providing exceptional, patient-first dental treatments with cutting-edge technology and genuine human warmth. Your smile is our lifelong masterpiece.', '© 2026 Mount Dental Care & Clinic. All rights reserved.', 'Mon-Sat : Morning - 10.00 AM - 01.00 PM | Evening 05.00 PM - 08.30 PM', '917010823417');

-- --------------------------------------------------------

--
-- Table structure for table `clinic_sitetext`
--

CREATE TABLE `clinic_sitetext` (
  `id` bigint(20) NOT NULL,
  `key` varchar(140) NOT NULL,
  `label` varchar(200) NOT NULL,
  `group` varchar(40) NOT NULL,
  `value` longtext NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_sitetext`
--

INSERT INTO `clinic_sitetext` (`id`, `key`, `label`, `group`, `value`, `sort_order`) VALUES
(1, 'hero.metric_1_label', 'Hero metric 1 label', 'hero', 'Experienced Dentists', 0),
(2, 'hero.metric_2_label', 'Hero metric 2 label', 'hero', 'Advanced Equipment', 1),
(3, 'hero.metric_3_label', 'Hero metric 3 label', 'hero', 'Affordable Care Plans', 2),
(4, 'hero.metric_4_label', 'Hero metric 4 label', 'hero', 'Happy Patients Served', 3),
(5, 'hero.book_button', 'Hero – Book Appointment button', 'hero', 'Book Appointment', 4),
(6, 'hero.call_button', 'Hero – Call Now button', 'hero', 'Call Now', 5),
(7, 'header.book_button', 'Header – Book Appointment button', 'header', 'Book Appointment', 6),
(8, 'offer.button_text', 'Offer banner button', 'offer', 'Book Today', 7),
(9, 'services.heading.eyebrow', 'Services heading eyebrow', 'services', 'WORLD-CLASS DENTAL CARE', 8),
(10, 'services.heading.title', 'Services heading title', 'services', 'Comprehensive Dental Services for Every Age', 9),
(11, 'services.heading.text', 'Services heading description', 'services', 'From preventative hygiene to intricate smile makeovers, our clinic utilizes state-of-the-art dental technology to ensure painless, lasting outcomes.', 10),
(12, 'services.learn_more', 'Service card link', 'services', 'Learn More', 11),
(13, 'services.cta.question', 'Services CTA question', 'services', 'Not sure which treatment suits your smile best?', 12),
(14, 'services.cta.button', 'Services CTA button', 'services', 'Schedule a 15-Minute Diagnostic Consultation', 13),
(15, 'services.modal.highlights_title', 'Popup highlights heading', 'services', 'Treatment Highlights & What\'s Included', 14),
(16, 'services.modal.book_button', 'Popup book button', 'services', 'Book Appointment For This Service', 15),
(17, 'services.modal.close_button', 'Popup close button', 'services', 'Close', 16),
(18, 'about.mission.title', 'Mission card title', 'about', 'Our Mission', 17),
(19, 'about.mission.text', 'Mission card text', 'about', 'To deliver exceptional, transparent, and comfortable, gentle dental healthcare that preserves natural smiles and uplifts self-esteem.', 18),
(20, 'about.vision.title', 'Vision card title', 'about', 'Our Vision', 19),
(21, 'about.vision.text', 'Vision card text', 'about', 'To become the community\'s lifelong oral health home, renowned for clinical precision, integrity, and warmth.', 20),
(22, 'experts.founder_tag', 'Lead doctor badge', 'experts', 'Lead Dentist & Founder', 21),
(23, 'experts.education_label', 'Credential – Education label', 'experts', 'Education & Credentials', 22),
(24, 'experts.tenure_label', 'Credential – Tenure label', 'experts', 'Clinical Tenure', 23),
(25, 'experts.expertise_label', 'Credential – Expertise label', 'experts', 'Core Expertise', 24),
(26, 'experts.membership_label', 'Credential – Membership label', 'experts', 'Indian Membership', 25),
(27, 'experts.book_button', 'Book with doctor button', 'experts', 'Book with', 26),
(28, 'experts.next_available', 'Next available note', 'experts', 'Next Available: Today at 3:30 PM', 27),
(29, 'awards.heading.eyebrow', 'Awards heading eyebrow', 'awards', 'ACADEMIC HONORS & RECOGNITIONS', 28),
(30, 'awards.heading.title', 'Awards heading title', 'awards', 'Awards & Scientific Achievements', 29),
(31, 'awards.heading.text', 'Awards heading description', 'awards', 'Honoring Dr. S. Natesh\'s distinguished research contributions, forensic odontology achievements, and leadership in dental clinical education.', 30),
(32, 'appointment.form_title', 'Booking form title', 'appointment', 'Book Your Appointment', 31),
(33, 'appointment.form_subtitle', 'Booking form subtitle', 'appointment', 'Fill in the details below to request a convenient time slot.', 32),
(34, 'appointment.bullet_1', 'Booking benefit 1', 'appointment', 'Personalized initial consultation for new patients', 33),
(35, 'appointment.bullet_2', 'Booking benefit 2', 'appointment', 'Instant Email verification & calendar confirmation', 34),
(36, 'appointment.bullet_3', 'Booking benefit 3', 'appointment', 'Prefer calling? Our reception team is happy to help you book a convenient slot.', 35),
(37, 'appointment.field.name.label', 'Form label – name', 'appointment', 'FULL NAME *', 36),
(38, 'appointment.field.name.placeholder', 'Form placeholder – name', 'appointment', 'John Doe', 37),
(39, 'appointment.field.mobile.label', 'Form label – mobile', 'appointment', 'MOBILE NUMBER *', 38),
(40, 'appointment.field.mobile.placeholder', 'Form placeholder – mobile', 'appointment', '+91 98765 43210', 39),
(41, 'appointment.field.email.label', 'Form label – email', 'appointment', 'EMAIL ADDRESS *', 40),
(42, 'appointment.field.email.placeholder', 'Form placeholder – email', 'appointment', 'john@example.com', 41),
(43, 'appointment.field.date.label', 'Form label – date', 'appointment', 'PREFERRED DATE *', 42),
(44, 'appointment.field.date.placeholder', 'Form placeholder – date', 'appointment', 'dd/mm/yyyy', 43),
(45, 'appointment.field.message.label', 'Form label – message', 'appointment', 'ADDITIONAL MESSAGE OR SYMPTOMS', 44),
(46, 'appointment.field.message.placeholder', 'Form placeholder – message', 'appointment', 'Tell us if you have toothache, sensitivity, or specific goals...', 45),
(47, 'appointment.field.treatment.label', 'Form label – treatment', 'appointment', 'TREATMENT TYPE *', 46),
(48, 'appointment.field.treatment.placeholder', 'Form dropdown placeholder', 'appointment', 'Select Dental Service', 47),
(49, 'appointment.submit', 'Booking submit button', 'appointment', 'Confirm & Book Appointment', 48),
(50, 'appointment.privacy', 'Booking privacy note', 'appointment', 'Your information is securely verified by email before the appointment is created.', 49),
(51, 'appointment.otp.step', 'OTP popup – step label', 'appointment', 'STEP 1 OF 2 • INSTANT EMAIL VERIFICATION', 50),
(52, 'appointment.otp.title', 'OTP popup – title', 'appointment', 'Verify Your Email Address', 51),
(53, 'appointment.otp.subtitle', 'OTP popup – subtitle (email appended)', 'appointment', 'Enter the 4-digit verification code sent by Gmail to', 52),
(54, 'appointment.otp.summary', 'OTP popup – summary label', 'appointment', 'Appointment • Preferred Date:', 53),
(55, 'appointment.otp.edit', 'OTP popup – edit button', 'appointment', 'Edit / Change', 54),
(56, 'appointment.otp.code_label', 'OTP popup – code label', 'appointment', 'ENTER 4-DIGIT CODE', 55),
(57, 'appointment.otp.valid_for', 'OTP popup – validity label', 'appointment', 'Code valid for', 56),
(58, 'appointment.otp.expired', 'OTP popup – expired note', 'appointment', 'This code has expired — request a new one.', 57),
(59, 'appointment.otp.resend_question', 'OTP popup – resend question', 'appointment', 'Didn\'t receive the code?', 58),
(60, 'appointment.otp.resend_in', 'OTP popup – resend countdown label', 'appointment', 'Resend in', 59),
(61, 'appointment.otp.resend_ready', 'OTP popup – resend ready note', 'appointment', 'You can resend now', 60),
(62, 'appointment.otp.resend_button', 'OTP popup – resend button', 'appointment', 'Resend code', 61),
(63, 'appointment.otp.resend_sending', 'OTP popup – resend busy label', 'appointment', 'Sending...', 62),
(64, 'appointment.otp.sent_note', 'OTP popup – delivery note', 'appointment', 'One email with your code was sent — check your Gmail inbox and spam folder.', 63),
(65, 'appointment.otp.demo_prefix', 'OTP popup – demo code prefix', 'appointment', 'Demo code:', 64),
(66, 'appointment.otp.submit', 'OTP popup – confirm button', 'appointment', 'Verify & Submit Appointment', 65),
(67, 'appointment.otp.verifying', 'OTP popup – verifying label', 'appointment', 'Verifying...', 66),
(68, 'appointment.otp.secure', 'OTP popup – security note', 'appointment', 'Secure email verification • Your information is protected', 67),
(69, 'appointment.success.title', 'Thanks popup – title', 'appointment', 'Appointment Request Received!', 68),
(70, 'appointment.success.text', 'Thanks popup – message', 'appointment', 'Our patient care team will contact you shortly to confirm.', 69),
(71, 'contact.call_label', 'Contact – call label', 'contact', 'CALL DIRECTLY', 70),
(72, 'contact.email_label', 'Contact – email label', 'contact', 'EMAIL SUPPORT', 71),
(73, 'contact.locations_label', 'Contact – locations label', 'contact', 'CLINIC LOCATIONS', 72),
(74, 'contact.directions', 'Get directions link', 'contact', 'Get Directions', 73),
(75, 'contact.hero_note', 'Contact sidebar note', 'contact', 'Our care coordinators reply within 15 minutes during clinic hours.', 74),
(76, 'phone_modal.title', 'Phone chooser title', 'header', 'Call Mount Dental Care', 75),
(77, 'phone_modal.description', 'Phone chooser description', 'header', 'Select a branch below to connect directly with our reception team:', 76),
(78, 'footer.quick_links_title', 'Footer – quick links heading', 'footer', 'QUICK LINKS', 77),
(79, 'footer.treatments_title', 'Footer – treatments heading', 'footer', 'KEY TREATMENTS', 78),
(80, 'footer.hours_title', 'Footer – hours heading', 'footer', 'CLINIC HOURS', 79);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_trustfeature`
--

CREATE TABLE `clinic_trustfeature` (
  `id` bigint(20) NOT NULL,
  `icon` varchar(40) NOT NULL,
  `title` varchar(150) NOT NULL,
  `description` longtext NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_trustfeature`
--

INSERT INTO `clinic_trustfeature` (`id`, `icon`, `title`, `description`, `sort_order`, `active`) VALUES
(1, 'award', 'Experienced Dental Specialists', 'Endodontists, implantologists and pediatric dental specialists with over 21+ years of combined mastery.', 0, 1),
(2, 'cpu', 'Advanced Dental Technology', 'Equipped with 3D CBCT scanners, intraoral scanners and computer-guided laser dentistry for precise diagnosis and digital treatment planning.', 1, 1),
(3, 'feather', 'Comfortable Procedures', 'Gentle injection techniques, nitrous oxide sedation options and calming noise-cancelling headsets.', 2, 1),
(4, 'sparkle', 'Hygienic Environment', 'Hospital-grade 5-stage autoclave sterilization protocols, HEPA-filtered operatory suites and single-use kits.', 3, 1),
(5, 'clipboard', 'Personalized Treatment Plans', 'Transparent upfront cost estimates with no hidden fees, flexible treatment options and affordable dental care plans designed around your needs and budget.', 4, 1),
(6, 'bell', 'Priority Dental Support', 'Fast telephone assistance and priority scheduling for patients looking for a same-day dental appointment.', 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `clinic_youtubevideo`
--

CREATE TABLE `clinic_youtubevideo` (
  `id` bigint(20) NOT NULL,
  `title` varchar(150) NOT NULL,
  `url` varchar(600) NOT NULL,
  `sort_order` int(10) UNSIGNED NOT NULL CHECK (`sort_order` >= 0),
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clinic_youtubevideo`
--

INSERT INTO `clinic_youtubevideo` (`id`, `title`, `url`, `sort_order`, `active`) VALUES
(1, 'Mount Dental Care - Clinic Tour', 'https://www.youtube.com/embed/65tuw4Y7RU0', 0, 1),
(2, 'Mount Dental Care - Patient Experience', 'https://www.youtube.com/embed/GLrd0jHBkc0', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(19, 'clinic', 'appointment'),
(24, 'clinic', 'award'),
(25, 'clinic', 'branch'),
(14, 'clinic', 'clinicaddress'),
(15, 'clinic', 'clinichour'),
(26, 'clinic', 'clinicimage'),
(12, 'clinic', 'doctor'),
(23, 'clinic', 'emaillog'),
(21, 'clinic', 'emailotp'),
(18, 'clinic', 'emailtemplate'),
(16, 'clinic', 'footerlink'),
(13, 'clinic', 'galleryitem'),
(22, 'clinic', 'herobanner'),
(8, 'clinic', 'navitem'),
(20, 'clinic', 'notification'),
(9, 'clinic', 'offerbanner'),
(17, 'clinic', 'pagecontent'),
(10, 'clinic', 'service'),
(7, 'clinic', 'sitesettings'),
(27, 'clinic', 'sitetext'),
(11, 'clinic', 'trustfeature'),
(28, 'clinic', 'youtubevideo'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-09-21 11:04:10.426131'),
(2, 'auth', '0001_initial', '2026-09-21 11:04:10.916985'),
(3, 'admin', '0001_initial', '2026-09-21 11:04:11.078588'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-09-21 11:04:11.101280'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-09-21 11:04:11.116279'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-09-21 11:04:11.211644'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-09-21 11:04:11.292718'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-09-21 11:04:11.320540'),
(9, 'auth', '0004_alter_user_username_opts', '2026-09-21 11:04:11.328986'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-09-21 11:04:11.417210'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-09-21 11:04:11.421212'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-09-21 11:04:11.435543'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-09-21 11:04:11.453123'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-09-21 11:04:11.485052'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-09-21 11:04:11.503576'),
(16, 'auth', '0011_update_proxy_permissions', '2026-09-21 11:04:11.527379'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-09-21 11:04:11.550083'),
(18, 'clinic', '0001_initial', '2026-09-21 11:04:12.057522'),
(19, 'clinic', '0002_herobanner', '2026-09-21 11:04:12.073167'),
(20, 'clinic', '0003_seed_email_templates', '2026-09-21 11:04:12.125954'),
(21, 'clinic', '0004_alter_emailtemplate_options_and_more', '2026-09-21 11:04:12.148831'),
(22, 'clinic', '0005_notification_guest_email', '2026-09-21 11:04:12.605484'),
(23, 'clinic', '0006_email_log_and_patient_message', '2026-09-21 11:04:12.772001'),
(24, 'clinic', '0007_otp_only_email_templates', '2026-09-21 11:04:12.809004'),
(25, 'clinic', '0008_alter_emailtemplate_body_and_more', '2026-09-21 11:04:12.827429'),
(26, 'clinic', '0009_alter_sitesettings_alternate_phone_and_more', '2026-09-21 11:04:12.853486'),
(27, 'clinic', '0010_award_branch_clinicimage_sitetext_youtubevideo_and_more', '2026-09-21 11:04:13.124190'),
(28, 'clinic', '0011_remove_service_duration_remove_service_suitable_for', '2026-09-21 11:04:13.155535'),
(29, 'clinic', '0012_alter_emailtemplate_options_alter_emailtemplate_body_and_more', '2026-09-21 11:04:13.290330'),
(30, 'clinic', '0013_remove_navitem_anchor_alter_navitem_label', '2026-09-21 11:04:13.358887'),
(31, 'clinic', '0014_footer_accreditation_and_copyright', '2026-09-21 11:04:13.403837'),
(32, 'clinic', '0015_remove_footer_badges_and_legal_links', '2026-09-21 11:04:13.459075'),
(33, 'clinic', '0016_remove_vamsi_lavu_and_kamalakannan_doctors', '2026-09-21 11:04:13.505487'),
(34, 'clinic', '0017_remove_unused_admin_content', '2026-09-21 11:04:13.719839'),
(35, 'sessions', '0001_initial', '2026-09-21 11:04:13.749368');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `clinic_appointment`
--
ALTER TABLE `clinic_appointment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `clinic_appointment_user_id_8bec0ee0_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `clinic_award`
--
ALTER TABLE `clinic_award`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_branch`
--
ALTER TABLE `clinic_branch`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_clinicaddress`
--
ALTER TABLE `clinic_clinicaddress`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_clinichour`
--
ALTER TABLE `clinic_clinichour`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_clinicimage`
--
ALTER TABLE `clinic_clinicimage`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_doctor`
--
ALTER TABLE `clinic_doctor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_emaillog`
--
ALTER TABLE `clinic_emaillog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `clinic_emaillog_appointment_id_f4e086c4_fk_clinic_appointment_id` (`appointment_id`),
  ADD KEY `clinic_emaillog_user_id_e38c9655_fk_auth_user_id` (`user_id`),
  ADD KEY `clinic_emaillog_recipient_9c680938` (`recipient`);

--
-- Indexes for table `clinic_emailotp`
--
ALTER TABLE `clinic_emailotp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `clinic_emailotp_user_id_354f8dc4_fk_auth_user_id` (`user_id`),
  ADD KEY `clinic_emailotp_email_93b0a62f` (`email`);

--
-- Indexes for table `clinic_emailtemplate`
--
ALTER TABLE `clinic_emailtemplate`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `template_type` (`template_type`);

--
-- Indexes for table `clinic_footerlink`
--
ALTER TABLE `clinic_footerlink`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_galleryitem`
--
ALTER TABLE `clinic_galleryitem`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_herobanner`
--
ALTER TABLE `clinic_herobanner`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_navitem`
--
ALTER TABLE `clinic_navitem`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_notification`
--
ALTER TABLE `clinic_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `clinic_notification_appointment_id_b2a4548b_fk_clinic_ap` (`appointment_id`),
  ADD KEY `clinic_notification_user_id_1ce0cc72_fk_auth_user_id` (`user_id`),
  ADD KEY `clinic_notification_email_6446077a` (`email`);

--
-- Indexes for table `clinic_offerbanner`
--
ALTER TABLE `clinic_offerbanner`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_pagecontent`
--
ALTER TABLE `clinic_pagecontent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key` (`key`);

--
-- Indexes for table `clinic_service`
--
ALTER TABLE `clinic_service`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_sitesettings`
--
ALTER TABLE `clinic_sitesettings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_sitetext`
--
ALTER TABLE `clinic_sitetext`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key` (`key`);

--
-- Indexes for table `clinic_trustfeature`
--
ALTER TABLE `clinic_trustfeature`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinic_youtubevideo`
--
ALTER TABLE `clinic_youtubevideo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clinic_appointment`
--
ALTER TABLE `clinic_appointment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clinic_award`
--
ALTER TABLE `clinic_award`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `clinic_branch`
--
ALTER TABLE `clinic_branch`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `clinic_clinicaddress`
--
ALTER TABLE `clinic_clinicaddress`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `clinic_clinichour`
--
ALTER TABLE `clinic_clinichour`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `clinic_clinicimage`
--
ALTER TABLE `clinic_clinicimage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `clinic_doctor`
--
ALTER TABLE `clinic_doctor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `clinic_emaillog`
--
ALTER TABLE `clinic_emaillog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clinic_emailotp`
--
ALTER TABLE `clinic_emailotp`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clinic_emailtemplate`
--
ALTER TABLE `clinic_emailtemplate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `clinic_footerlink`
--
ALTER TABLE `clinic_footerlink`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `clinic_galleryitem`
--
ALTER TABLE `clinic_galleryitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `clinic_herobanner`
--
ALTER TABLE `clinic_herobanner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `clinic_navitem`
--
ALTER TABLE `clinic_navitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `clinic_notification`
--
ALTER TABLE `clinic_notification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clinic_offerbanner`
--
ALTER TABLE `clinic_offerbanner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `clinic_pagecontent`
--
ALTER TABLE `clinic_pagecontent`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `clinic_service`
--
ALTER TABLE `clinic_service`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `clinic_sitesettings`
--
ALTER TABLE `clinic_sitesettings`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `clinic_sitetext`
--
ALTER TABLE `clinic_sitetext`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `clinic_trustfeature`
--
ALTER TABLE `clinic_trustfeature`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `clinic_youtubevideo`
--
ALTER TABLE `clinic_youtubevideo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `clinic_appointment`
--
ALTER TABLE `clinic_appointment`
  ADD CONSTRAINT `clinic_appointment_user_id_8bec0ee0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `clinic_emaillog`
--
ALTER TABLE `clinic_emaillog`
  ADD CONSTRAINT `clinic_emaillog_appointment_id_f4e086c4_fk_clinic_appointment_id` FOREIGN KEY (`appointment_id`) REFERENCES `clinic_appointment` (`id`),
  ADD CONSTRAINT `clinic_emaillog_user_id_e38c9655_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `clinic_emailotp`
--
ALTER TABLE `clinic_emailotp`
  ADD CONSTRAINT `clinic_emailotp_user_id_354f8dc4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `clinic_notification`
--
ALTER TABLE `clinic_notification`
  ADD CONSTRAINT `clinic_notification_appointment_id_b2a4548b_fk_clinic_ap` FOREIGN KEY (`appointment_id`) REFERENCES `clinic_appointment` (`id`),
  ADD CONSTRAINT `clinic_notification_user_id_1ce0cc72_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
