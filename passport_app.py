import streamlit as st
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
import os

# Function to resize image to passport size
def resize_to_passport_size(image_path):
    passport_size = (75, 100)  # 100px x 100px for passport photo
    img = Image.open(image_path)
    img = img.resize(passport_size, Image.Resampling.LANCZOS)  # Resize with high-quality filtering
    return img

# Function to create a PDF with 6 passport-sized photos in a single row
def create_passport_photos_pdf(input_image_path, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)  # A4 size (595x842)

    # Resize the input image
    img = resize_to_passport_size(input_image_path)

    # Calculate the starting position and space between images
    x_start = 10  # Starting x position for the first image
    y_offset = 680  # y position from the top for the row (you can adjust this as needed)

    # Horizontal space between images
    x_space = 90  # Space between images horizontally

    # Loop to place 6 images in a single row
    for i in range(6):
        # Calculate the x position for each image
        x_offset = x_start + i * x_space

        # Save resized image as a temporary file
        temp_image_path = f"temp_image_{i}.png"
        img.save(temp_image_path)

        # Set stroke color and line width for the border
        c.setStrokeColor(black)  # Black border
        c.setLineWidth(2)  # Stroke thickness of 2

        # Draw a rectangle around the image (border)
        c.rect(x_offset - 2, y_offset - 2, img.width + 4, img.height + 4)  # Add 4px to width/height for border

        # Draw the image onto the PDF canvas
        c.drawImage(temp_image_path, x_offset, y_offset, width=img.width, height=img.height)

        # Clean up temporary files
        os.remove(temp_image_path)  # Remove temporary image file

    # Finalize the PDF document
    c.save()

# Streamlit UI
def main():
    st.title("6 Passport Size Photos Maker in One Line with Border")

    # Display link at the top for background removal
    st.markdown(
        """
        ### Want to remove the background from your image?
        You can easily remove the background and set it to white by visiting [remove.bg](https://www.remove.bg/t/change-background).
        Simply upload your image there, and follow the instructions to change the background to white!
        """
    )
    
    # File uploader for the user to upload an image
    uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded image to a temporary file
        image_path = os.path.join("temp_image.jpg")
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display the uploaded image
        st.image(image_path, caption="Uploaded Image", use_container_width=True)
        
        # Button to generate PDF
        if st.button("Generate Passport Photos PDF in One Line with Border"):
            output_pdf_path = "6_passport_photos_one_line_with_border.pdf"
            create_passport_photos_pdf(image_path, output_pdf_path)
            
            # Provide download link for the PDF
            with open(output_pdf_path, "rb") as f:
                st.download_button(
                    label="Download 6 Passport Photos PDF",
                    data=f,
                    file_name="6_passport_photos_one_line_with_border.pdf",
                    mime="application/pdf"
                )
            st.success("PDF created successfully with 6 photos in one line!")

if __name__ == "__main__":
    main()
