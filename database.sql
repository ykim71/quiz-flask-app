CREATE TABLE `quiz_log` (
  `id` int NOT NULL,
  `session_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `question_number` int DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  `variable_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `question` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `answer_string` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL
);

ALTER TABLE `quiz_log`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `quiz_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

CREATE TABLE `session_info` (
  `id` int NOT NULL,
  `session_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `page_load_time` datetime NOT NULL,
  `submission_time` datetime NOT NULL,
  `gender` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `education` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `age` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `religion` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `political_ideology` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `occupation` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `household_income` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `relationship` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `news_use` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `social_media_use` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL

);

ALTER TABLE `session_info`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `session_info`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
