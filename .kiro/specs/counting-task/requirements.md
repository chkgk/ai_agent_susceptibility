# Requirements Document

## Introduction

This feature adds a new oTree 5 app called "counting_task" that presents participants with a visual counting exercise. The app consists of two pages: an Instructions page for researcher-provided content and a Task page where participants count ones in a randomly generated binary table image and input their count.

## Requirements

### Requirement 1

**User Story:** As a researcher, I want to create a new oTree app with proper structure, so that I can run counting task experiments within the oTree framework.

#### Acceptance Criteria

1. WHEN the app is created THEN the system SHALL follow oTree 5 conventions with proper Subsession, Group, and Player models
2. WHEN the app is configured THEN the system SHALL include proper constants (NAME_IN_URL, PLAYERS_PER_GROUP, NUM_ROUNDS)
3. WHEN the app is added to settings THEN the system SHALL be accessible through the oTree interface

### Requirement 2

**User Story:** As a researcher, I want an Instructions page in the app, so that I can provide participants with task instructions before they begin.

#### Acceptance Criteria

1. WHEN the Instructions page is accessed THEN the system SHALL display a template that I can customize with instructions
2. WHEN the Instructions page is rendered THEN the system SHALL follow oTree 5 HTML template conventions
3. WHEN participants view the Instructions page THEN the system SHALL provide a next button to proceed to the task

### Requirement 3

**User Story:** As a researcher, I want a Task page that displays a binary table image, so that participants can perform the counting exercise.

#### Acceptance Criteria

1. WHEN the Task page loads THEN the system SHALL generate a random binary table with zeros and ones
2. WHEN the binary table is generated THEN the system SHALL create an image representation of the table
3. WHEN the image is created THEN the system SHALL display it on the Task page template
4. WHEN the Task page renders THEN the system SHALL include the generated image in the HTML template

### Requirement 4

**User Story:** As a participant, I want to input my count of ones, so that I can submit my answer for the counting task.

#### Acceptance Criteria

1. WHEN the Task page displays THEN the system SHALL provide an input field for entering the number of ones
2. WHEN I enter a number THEN the system SHALL accept numeric input only
3. WHEN I submit my answer THEN the system SHALL store the value in the Player model's "counted_ones" field
4. WHEN the form is submitted THEN the system SHALL validate the input and proceed to the next page

### Requirement 5

**User Story:** As a researcher, I want the binary table generation to be randomized, so that each participant sees a different counting challenge.

#### Acceptance Criteria

1. WHEN a new participant accesses the Task page THEN the system SHALL generate a unique random distribution of ones and zeros
2. WHEN the table is generated THEN the system SHALL ensure a random number of ones is placed in the table
3. WHEN the table is created THEN the system SHALL fill all non-one positions with zeros
4. WHEN the randomization occurs THEN the system SHALL ensure reproducible results within the same session if needed

### Requirement 6

**User Story:** As a researcher, I want the counting data recorded properly, so that I can analyze participant performance.

#### Acceptance Criteria

1. WHEN a participant submits their count THEN the system SHALL store the value in the Player model's "counted_ones" field
2. WHEN the data is stored THEN the system SHALL ensure the field accepts integer values
3. WHEN the session completes THEN the system SHALL make the counted_ones data available for export
4. WHEN multiple participants complete the task THEN the system SHALL maintain separate records for each participant