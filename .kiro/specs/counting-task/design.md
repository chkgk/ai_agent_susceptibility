# Design Document

## Overview

The counting_task app will be implemented as a standard oTree 5 application following the established patterns from the header_demo app. The app will generate binary table images server-side using Python's built-in libraries and serve them through oTree's static file system. The core functionality centers around random binary table generation, image creation, and form-based data collection.

## Architecture

The app follows oTree 5's standard MVC architecture:

- **Models**: Subsession, Group, and Player classes with Player containing the `counted_ones` field
- **Views**: Two page classes (Instructions and Task) handling the page flow
- **Templates**: HTML templates for each page following oTree conventions
- **Static Assets**: Generated binary table images stored in the app's static directory

### Component Flow

1. Instructions page displays researcher-provided content
2. Task page triggers binary table generation in the backend
3. Generated image is saved to static directory and referenced in template
4. User input is captured via oTree form field and stored in Player model
5. Page sequence manages navigation between Instructions and Task pages

## Components and Interfaces

### Models

**Constants (C class)**
- `NAME_IN_URL = 'counting_task'`
- `PLAYERS_PER_GROUP = None` (individual task)
- `NUM_ROUNDS = 1`

**Player Model**
- `counted_ones`: IntegerField to store participant's count input
- `correct_ones`: Computed field to store the actual count of ones in the table
- `image_path`: StringField to store the path of the generated image
- Inherits from BasePlayer following oTree conventions

**Subsession and Group Models**
- Standard empty implementations inheriting from BaseSubsession and BaseGroup
- No additional fields required for this task

### Views (Pages)

**Instructions Page**
- Simple page class inheriting from Page
- No special logic required
- Displays static content from template
- Implements a `before_next_page()` method:
    - Generate random binary table
    - Create image representation
    - Save image to static directory
    - Store the image path and actual count on the Player


**Task Page**
- Inherits from Page
- Implements `vars_for_template()` method to:
  - Pass the image path to the template
- Includes form field for `counted_ones` input

### Image Generation System

**Binary Table Generator**
- Function to create NxN grid (e.g., 10x10)
- Random placement of ones (random count between configurable min/max)
- Fill remaining cells with zeros
- Return both the table data and actual count of ones

**Image Creator**
- Use Python's built-in libraries (no external dependencies)
- Generate simple grid visualization:
  - White background
  - Black borders for cells
  - "1" text in cells containing ones
  - "0" text in cells containing zeros
- Save as PNG to app's static directory
- Return relative path for template inclusion

## Data Models

### Player Model Fields

```python
class Player(BasePlayer):
    counted_ones = models.IntegerField(
        label="How many ones do you count in the image?",
        blank=True,
        null=True
    )
    correct_ones = models.IntegerField(
        blank=True,
        null=True
    )
    image_path = models.StringField(
        blank=True,
        null=True
    )
```

**Field Specifications:**
- `counted_ones`: Stores the participant's input count of ones from the binary table image
- `correct_ones`: Stores the actual number of ones in the generated table for accuracy analysis
- `image_path`: Stores the relative path to the generated image file for reference and potential cleanup
- All fields use `blank=True, null=True` to allow for incomplete submissions during development/testing
- Validation will be handled at the form level rather than model level for better user experience

### Binary Table Structure

- 2D list/array representing the grid
- Each cell contains either 0 or 1
- Grid size: 10x10 (configurable)
- Number of ones: Random between 5-25 (configurable)

### Image Specifications

- Format: PNG
- Size: 400x400 pixels (40px per cell for 10x10 grid)
- Cell styling: Black border, white background
- Text: Clear, readable numbers centered in each cell
- Filename: Unique per participant/session to avoid conflicts

## Error Handling

### Image Generation Errors
- Log errors for debugging
- Ensure graceful degradation

### File System Errors
- Clean up temporary files
- Provide meaningful error messages

### Input Validation
- Ensure counted_ones accepts only valid integers
- Handle edge cases (negative numbers, non-numeric input)
- Provide clear validation messages

### Static File Serving
- Ensure proper URL generation for images
- Handle missing image files gracefully
- Clean up old images to prevent storage bloat

## Testing Strategy

### Unit Tests
- Binary table generation logic
- Image creation functionality
- Input validation for counted_ones field
- Static file path generation

### Integration Tests
- Full page rendering with generated images
- Form submission and data storage
- Page sequence navigation
- Static file serving

### Manual Testing
- Visual verification of generated images
- Cross-browser compatibility for image display
- Form functionality across different input scenarios
- Performance with multiple concurrent users

### Test Data Scenarios
- Various grid sizes and one counts
- Edge cases (all zeros, all ones, single one)
- Multiple participants generating different images
- Form validation with invalid inputs

## Implementation Considerations

### Performance
- Generate images on-demand rather than pre-generating
- Consider caching strategies for identical configurations
- Optimize image size for web delivery
- Clean up old images periodically

### Scalability
- Unique image filenames to prevent conflicts
- Efficient random number generation
- Minimal memory usage during image creation

### Maintainability
- Configurable parameters (grid size, one count range)
- Clear separation between table generation and image creation
- Reusable components for potential future enhancements

### oTree 5 Compliance
- Follow established patterns from header_demo app
- Use standard oTree form handling
- Maintain consistent template structure
- Proper integration with oTree's static file system