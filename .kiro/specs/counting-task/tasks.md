# Implementation Plan

- [x] 1. Create basic app structure and models
  - Create counting_task directory and __init__.py file with oTree 5 structure
  - Implement Subsession, Group, and Player models following header_demo patterns
  - Add counted_ones, correct_ones, and image_path fields to Player model
  - _Requirements: 1.1, 1.2, 6.1, 6.2_

- [x] 2. Implement binary table generation functionality
  - Create function to generate random NxN binary table with configurable parameters
  - Implement logic to randomly place specified number of ones in the table
  - Fill remaining cells with zeros and return both table data and actual count
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 3. Create image generation system
  - Implement function to convert binary table data into PNG image
  - Use Python built-in libraries to create grid visualization with cell borders
  - Add text rendering for "0" and "1" values in appropriate cells
  - Save generated images to app's static directory with unique filenames
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 4. Implement Instructions page
  - Create Instructions page class inheriting from Page
  - Create Instructions.html template following oTree 5 conventions
  - Add placeholder content that researchers can customize
  - Include proper next button for navigation
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 5. Implement Task page with image display
  - Create Task page class with vars_for_template method
  - Integrate binary table generation and image creation in page logic
  - Store correct_ones and image_path values in Player model
  - Return image path and necessary data to template context
  - _Requirements: 3.1, 3.2, 3.4, 6.1_

- [x] 6. Create Task page template with form
  - Create Task.html template displaying the generated image
  - Add form field for counted_ones input with proper labeling
  - Include form validation and next button functionality
  - Follow oTree 5 template conventions for form handling
  - _Requirements: 4.1, 4.2, 4.4_

- [ ] 7. Configure page sequence and app integration
  - Set up page_sequence with Instructions and Task pages
  - Update settings.py to include counting_task app in SESSION_CONFIGS
  - Test basic navigation flow between pages
  - _Requirements: 1.3, 2.3_

- [ ] 8. Add form validation and data storage
  - Implement proper form field validation for counted_ones input
  - Ensure numeric input validation and error handling
  - Test data storage in Player model fields
  - Verify form submission triggers proper data saving
  - _Requirements: 4.2, 4.3, 6.2, 6.3_

- [ ] 9. Implement error handling and edge cases
  - Add error handling for image generation failures
  - Implement fallback mechanisms for file system errors
  - Handle edge cases in binary table generation
  - Add proper error messages for form validation
  - _Requirements: 5.4, 6.4_

- [ ] 10. Create unit tests for core functionality
  - Write tests for binary table generation logic
  - Test image creation and file saving functionality
  - Create tests for form validation and data storage
  - Test page rendering and template context
  - _Requirements: 1.1, 3.1, 4.3, 5.1_