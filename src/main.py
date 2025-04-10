# Final Project - Phiora.
from score import calculate_score
from face_shape import face_shape
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
import cv2
import os
import sys
import math

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def toggle_fullscreen():
    state = not app.attributes('-fullscreen')
    app.attributes('-fullscreen', state)
    if state:
        fullscreen_button.config(text="Exit Fullscreen")
    else:
        fullscreen_button.config(text="Fullscreen")

def update_score_gauge(score):
    # Clear the canvas
    gauge_canvas.delete("all")
    
    # Calculate angle based on score (0-10)
    angle = 180 - (score / 10 * 180)
    
    # Draw gauge background
    gauge_canvas.create_arc(10, 10, 190, 190, start=0, extent=180, fill="#444444", outline="#2a2a2a", width=2)
    
    # Determine color based on score
    if score >= 8:
        color = "#4CAF50"  # Green
    elif score >= 6:
        color = "#FFC107"  # Yellow
    else:
        color = "#F44336"  # Red
    
    # Draw score indicator
    gauge_canvas.create_arc(10, 10, 190, 190, start=180, extent=-180+angle, fill=color, outline=color)
    
    # Draw center circle
    gauge_canvas.create_oval(100-8, 100-8, 100+8, 100+8, fill="#2a2a2a", outline="#777777")
    
    # Draw score text
    gauge_canvas.create_text(100, 130, text=f"{score:.1f}", fill="white", font=("Arial", 24, "bold"))
    gauge_canvas.create_text(100, 155, text="/10", fill="#aaaaaa", font=("Arial", 12))
    
    # Draw tick marks
    for i in range(11):
        angle_rad = math.radians(180 - (i / 10 * 180) + 180)
        start_x = 100 + 85 * math.cos(angle_rad)
        start_y = 100 + 85 * math.sin(angle_rad)
        end_x = 100 + 75 * math.cos(angle_rad)
        end_y = 100 + 75 * math.sin(angle_rad)
        
        if i == int(score):
            width = 3
        else:
            width = 1
            
        gauge_canvas.create_line(start_x, start_y, end_x, end_y, fill="white", width=width)
        
        # Add labels at 0, 5, and 10
        if i in [10, 5, 0]:
            label_x = 100 + 65 * math.cos(angle_rad)
            label_y = 100 + 65 * math.sin(angle_rad)

            # Swap labels for 10 and 0
            label_text = "0" if i == 10 else "10" if i == 0 else str(i)

            gauge_canvas.create_text(label_x, label_y, text=label_text, fill="white", font=("Arial", 10))

def generate_improvement_suggestions(ratios, deviations, tot_score):
    suggestions = []
    
    # Add overall score commentary
    if tot_score >= 8.5:
        suggestions.append("Your facial features show excellent proportion and harmony according to the golden ratio.")
    elif tot_score >= 7:
        suggestions.append("Your facial proportions show good harmony overall with some minor deviations from the golden ratio.")
    elif tot_score >= 5:
        suggestions.append("Your facial proportions have moderate harmony with some areas that could be enhanced.")
    else:
        suggestions.append("Your facial proportions have potential for enhancement in several areas.")
    
    # Check specific areas for improvement
    problem_areas = []
    for i, deviation in enumerate(deviations):
        if deviation > 0.3:  # Significant deviation
            problem_areas.append((i, deviation))
    
    # Sort problem areas by deviation (largest first)
    problem_areas.sort(key=lambda x: x[1], reverse=True)
    
    # Generate specific suggestions for top 3 problem areas
    for idx, _ in problem_areas[:3]:
        if idx == 0:  # Forehead to midface ratio
            if ratios[idx] > 1.618:
                suggestions.append("Consider hairstyles with bangs or side-swept layers to reduce forehead prominence. Eyebrow shaping to lift the arches can also help balance the upper and middle portions of your face.")
                suggestions.append("Consider hairstyles that add volume to the sides or reduce the height of your forehead. If you have facial hair, a fuller beard can help balance facial proportions.")
            else:
                suggestions.append("Hairstyles with volume at the crown or swept-back styles can enhance your forehead proportion. Highlighting the midface with subtle makeup contouring can also help create balance.")
                
                suggestions.append("Hairstyles with more height and less width can help enhance your facial proportions. Consider styles that expose more of your forehead.")
        
        elif idx == 1:  # Full face length to lower face ratio
            if ratios[idx] > 1.618:
                suggestions.append("A well-groomed beard or stubble can help balance the lower third of your face. Hairstyles with volume on the sides can create a more balanced appearance.")
            
                suggestions.append("Contouring techniques along the jawline and highlighting the cheekbones can help balance your facial proportions. Long earrings can also create a visual effect that balances face length.")
            else:
                
                suggestions.append("Emphasizing your cheekbones with highlighting and using blush slightly higher on your cheeks can create more balance in your facial proportions.")
            
                suggestions.append("Keeping facial hair shorter on the sides and slightly longer on the chin can help elongate your face. Hairstyles with height on top can also help.")
        
        elif idx == 2:  # Hairline to eyes vs eyes to chin
            if ratios[idx] > 1.618:
                suggestions.append("Curtain bangs or layered hairstyles that frame the face and defined eyebrow shaping can help balance the upper and lower portions of your face.")
                
                suggestions.append("Hairstyles with length on the sides and defined edges can help frame your face better. If you have facial hair, keeping it well-groomed can enhance your facial balance.")
            else:
                
                suggestions.append("Updos or hairstyles that add height at the crown can enhance your facial balance. Drawing attention to your eyes with makeup can also help.")
                
                suggestions.append("Hairstyles with more height and volume on top can help balance your facial proportions. Keeping the sides shorter creates a more balanced look.")
        
        elif idx == 3:  # Facial width to nose width
            if ratios[idx] > 1.618:
                suggestions.append("Makeup techniques like nose contouring (or camera angles for photos) can create the appearance of a more balanced nose width relative to your face width.")
            else:
                
                suggestions.append("Highlighting the outer edges of your face and contouring your cheeks can create a more balanced facial width proportion. Hairstyles that add width can also help.")
                
                suggestions.append("Hairstyles with more volume on the sides and facial hair styles that add width to the face can help create better proportion.")
        
        elif idx == 4:  # Eye distance to mouth width
            if ratios[idx] > 1.618:
                suggestions.append("Lip liner slightly outside your natural lip line or lipstick techniques to enhance lip fullness can help balance the proportion between your eyes and mouth.")
            
                suggestions.append("For photography, slightly turning your face rather than facing directly forward can create better proportions between your eyes and mouth.")
            else:
                
                suggestions.append("Eye makeup that enhances the outer corners of your eyes can help balance the proportion between your eyes and mouth. Consider winged eyeliner or eyeshadow techniques.")
                
                suggestions.append("Facial hair styles that are narrower on the sides can help create better balance between your eyes and mouth.")
    
    # Add general suggestions if we have few specific ones
    if len(suggestions) < 3:
        suggestions.append("Consider experimenting with different hairstyles, makeup techniques, or accessories to enhance your natural features.")
    
        suggestions.append("Consider experimenting with different hairstyles, facial hair styles, or grooming techniques to enhance your natural features.")
        
        suggestions.append("Professional portrait photographers often use lighting techniques to highlight your best features - consider a professional photoshoot to showcase your unique features.")
    
    # Add a positive closing note
    suggestions.append("Remember, these are just suggestions based on mathematical proportions. True beauty encompasses personality, expressiveness, and uniqueness that no algorithm can measure.")
    
    return suggestions

def upload_image():
    # Open a file dialog for the user to select an image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp;*.tiff;*.jfif;*.svg;*.ppm;*.pgm;*.heic;*.bpg;*.ico;*.jpe;*.jp2;*.jps;*.pbm;*.pcx;*.pic;*.pict;*.pnm;*.psd;*.rgb;*.rgba;*.tga;*.tif")]
    )
    if file_path:
        try:
            # Update status
            status_label.config(text="Processing image...", foreground="#FFD700")
            app.update()

            net = cv2.dnn.readNetFromCaffe(resource_path("models\\deploy.prototxt"), resource_path("models\\res10_300x300_ssd_iter_140000.caffemodel"))

            ratio, deviation, score, img_copy = calculate_score(file_path, net)
            # detected_gender = gender_detect(file_path, net)
            face_shape_result, hairstyle_recommendation = face_shape(file_path)

            hairstyle_text.config(state=tk.NORMAL)
            hairstyle_text.delete(1.0, tk.END)
            hairstyle_text.insert(tk.END, f"👤 Face Shape: {face_shape_result}\n\n", "heading")
            hairstyle_text.insert(tk.END, f"💇 Recommended Hairstyles:\n\n", "heading")
            hairstyle_text.insert(tk.END, hairstyle_recommendation)
            hairstyle_text.config(state=tk.DISABLED)

            suggestions = generate_improvement_suggestions(ratio, deviation, score)

            # Open and display the image in the GUI
            height = 400
            scale_factor = height / img_copy.shape[0]  # Calculate scale ratio
            width = int(img_copy.shape[1] * scale_factor)  # Maintain aspect ratio
            img = cv2.resize(img_copy, (width, height))
            img_copy_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_copy_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)

            # Hide the default message
            default_image_msg.pack_forget()

            # Show the image label
            image_label.pack(fill=tk.BOTH, expand=True)

            # Update the image label
            image_label.config(image=img_tk)
            image_label.image = img_tk  # Prevent garbage collection
           
            # Dynamically set the width of image_frame to match the image
            image_frame.config(width=width, height=height)
            hairstyle_frame.config(width=width)  # Match image width

            # Optional: force update to apply geometry changes
            image_frame.update_idletasks()
            hairstyle_frame.update_idletasks()

            # Display the score
            score_label.config(text=f"Golden Ratio Score: {score:.2f} / 10.0")
            
            # Update the gauge
            update_score_gauge(score)
            
            # Update suggestions text
            suggestions_text.config(state=tk.NORMAL)
            suggestions_text.delete(1.0, tk.END)
            suggestions_text.insert(tk.END, "💡 IMPROVEMENT SUGGESTIONS:\n\n", "heading")
            for suggestion in suggestions:
                suggestions_text.insert(tk.END, f"• {suggestion}\n\n", "suggestion")
            suggestions_text.config(state=tk.DISABLED)
            
            # Show analysis results
            analysis_text.config(state=tk.NORMAL)
            analysis_text.delete(1.0, tk.END)
            analysis_text.insert(tk.END, "📊 DETAILED ANALYSIS:\n\n", "heading")
            
            ratio_names = [
                "Face length to face width ratio",  # face length / face width
                "Head to pupils vs pupils to lips ratio",  # heads to pupils / pupils to lips
                "Nose tip to chin vs lips to chin ratio",  # nose tip to chin / lips to chin
                "Nose tip to chin vs pupils to nose tips ratio",  # nose tip to chin / pupils to nose tips
                "Nose width to nose tips to lips ratio",  # width of nose / nose tips to lips
                "Outer eye distance to hairline to pupils ratio",  # outside distance between eyes / hairline to pupils
                "Lip length to nose width ratio"  # length of lips / width of nose
            ]

            
            for i in range(len(ratio_names)):
                analysis_text.insert(tk.END, f"{ratio_names[i]}:\n", "subheading")
                analysis_text.insert(tk.END, f"   Measured: {ratio[i]:.3f}   (Golden ratio: 1.618)\n", "data")
                
                # Calculate percent match to golden ratio
                match_percent = (1 - deviation[i]/1.618) * 100
                match_percent = max(0, min(100, match_percent))
                
                # Color code based on how close to golden ratio
                if match_percent > 85:
                    tag = "good"
                elif match_percent > 70:
                    tag = "average"
                else:
                    tag = "poor"
                    
                analysis_text.insert(tk.END, f"   Match to golden ratio: {match_percent:.1f}%\n\n", tag)
            
            analysis_text.config(state=tk.DISABLED)
            
            # Update status
            status_label.config(text="Analysis complete!", foreground="#4CAF50")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the image.\n{e}")
            status_label.config(text="Error processing image", foreground="#FF5252")

def create_tooltip(widget, text):
    """Create a tooltip for a given widget"""
    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        
        # Create a toplevel window
        tip = tk.Toplevel(widget)
        tip.wm_overrideredirect(True)
        tip.wm_geometry(f"+{x}+{y}")
        tip.attributes('-topmost', True)
        
        label = tk.Label(tip, text=text, justify=tk.LEFT,
                         background="#333333", foreground="white", 
                         relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 10, "normal"), padx=5, pady=5)
        label.pack()
        
        widget.tooltip = tip

    def leave(event):
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# Main App Window
app = tk.Tk()
app.title("Phiora - Facial Harmony Analysis")

try:
    app.iconbitmap(resource_path('public\\phiora_logo.ico'))
except:
    pass

app.state('zoomed')
app.config(bg="#1a1a1a")

# Theme
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 12, 'bold'), background='#4CAF50', foreground='white')
style.configure('TFrame', background='#1a1a1a')
style.configure('Header.TLabel', font=('Arial', 20, 'bold'), background='#1a1a1a', foreground='white')
style.configure('TLabel', font=('Arial', 12), background='#1a1a1a', foreground='white')
style.configure('Status.TLabel', font=('Arial', 10), background='#1a1a1a', foreground='#aaaaaa')

# ========== HEADER ==========
header_frame = ttk.Frame(app)
header_frame.pack(fill=tk.X, padx=20, pady=10)

logo_label = ttk.Label(header_frame, text="PHIORA", style='Header.TLabel')
logo_label.pack(side=tk.LEFT)

fullscreen_button = tk.Button(header_frame, text="Fullscreen", command=toggle_fullscreen,
    font=("Arial", 10), bg="#333333", fg="white",
    activebackground="#555555", activeforeground="white", padx=8, pady=4)
fullscreen_button.pack(side=tk.RIGHT, padx=(10, 0))

# ========== MAIN CONTENT ==========
content_frame = ttk.Frame(app)
content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# ========== LEFT PANEL ==========
# Left panel - Control panel and gauge
left_panel = ttk.Frame(content_frame, width=400)
left_panel.pack_propagate(False)
left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

# Score gauge
gauge_frame = ttk.Frame(left_panel)
gauge_frame.pack(fill=tk.X, pady=(0, 20))

gauge_canvas = tk.Canvas(gauge_frame, width=200, height=180, bg="#2a2a2a", highlightthickness=0)
gauge_canvas.pack(pady=(10, 0))

# Update gauge with default values
update_score_gauge(0)

# Upload button
upload_button = ttk.Button(left_panel, text="Upload Photo", command=upload_image)
upload_button.pack(fill=tk.X, pady=10)
create_tooltip(upload_button, "Upload a photo for facial harmony analysis")

# Score label
score_label = ttk.Label(left_panel, text="Golden Ratio Score: -.-- / 10.0", font=("Arial", 14, "bold"))
score_label.pack(pady=5)

# Status label
status_label = ttk.Label(left_panel, text="Ready to analyze", style='Status.TLabel')
status_label.pack(pady=5)

# Information text box
info_frame = ttk.Frame(left_panel)
info_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

info_text = tk.Text(info_frame, wrap=tk.WORD, bg="#333333", foreground="#ffffff", font=("Arial", 10), 
                  borderwidth=1, relief=tk.SOLID, padx=10, pady=10, height=10)
info_text.pack(fill=tk.BOTH, expand=True)
info_text.insert(tk.END, "ℹ️ ABOUT THE GOLDEN RATIO\n\n", "heading")
info_text.insert(tk.END, "The golden ratio (around 1.618) is often associated with beauty, especially in facial proportions. This app analyzes your face and compares its symmetry and feature ratios to the golden ratio, giving you a score based on how closely they align. \n\nKeep in mind, beauty is subjective and influenced by many factors beyond numbers.")
info_text.config(state=tk.DISABLED)

# Add text tags
info_text.tag_configure("heading", font=("Arial", 12, "bold"), foreground="#4CAF50")

# ========== CENTER PANEL ==========
# Center panel - Image display
center_panel = ttk.Frame(content_frame)
center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

image_frame = ttk.Frame(center_panel, width=350, height=400)  # Set a default size
image_frame.pack_propagate(False)  # Prevent shrinking to fit content
image_frame.pack(pady=(0, 10))

# Message shown when no image is loaded
default_image_msg = ttk.Label(
    image_frame,
    text="📷 Please upload a clear photo of your face.\n\nKeep a straight face with minimal smile for accurate analysis.",
    background="#1f1f1f",
    foreground="#cccccc",
    wraplength=300,
    justify="center",
    font=("Arial", 15, "italic", "bold"),
    anchor="center"
)
default_image_msg.pack(fill=tk.BOTH, expand=True)

# Image label (hidden by default until image is uploaded)
image_label = ttk.Label(image_frame, background="#1f1f1f")
# image_label.pack(fill=tk.BOTH, expand=True)  # ⛔ Don't pack yet

# ========== HAIRSTYLE RECOMMENDATION ==========
hairstyle_frame = ttk.Frame(center_panel, height=200, width=350)
hairstyle_frame.pack_propagate(False)
hairstyle_frame.pack(pady=(0, 10), padx=20, fill=tk.BOTH)  # ✅ Pack here

# ScrolledText directly inside hairstyle_frame (removed inner_hairstyle_frame)
hairstyle_text = scrolledtext.ScrolledText(
    hairstyle_frame,
    wrap=tk.WORD,
    bg="#333333",
    foreground="#ffffff",
    font=("Arial", 10),
    borderwidth=1,
    relief=tk.SOLID,
    height=10, 
    padx=10, 
    pady=10
)
hairstyle_text.pack(fill=tk.BOTH, expand=True)

hairstyle_text.insert(tk.END, "👤 Face Shape: Unknown\n\n", "centered_heading")
hairstyle_text.insert(tk.END, "💇 Recommended Hairstyles:\n\n", "heading")
hairstyle_text.insert(tk.END, "Upload a photo to get hairstyle suggestions.")
hairstyle_text.config(state=tk.DISABLED)

# Text styling
hairstyle_text.tag_configure("heading", font=("Arial", 12, "bold"), foreground="#4CAF50")
hairstyle_text.tag_configure("centered_heading", font=("Arial", 12, "bold"), foreground="#4CAF50", justify="center")
hairstyle_text.tag_configure("suggestion", font=("Arial", 10), foreground="white")

# ========== RIGHT PANEL ==========
# Right panel - Analysis and suggestions
right_panel = ttk.Frame(content_frame)
right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

# Analysis details
analysis_frame = ttk.Frame(right_panel)
analysis_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

analysis_text = scrolledtext.ScrolledText(analysis_frame, wrap=tk.WORD, bg="#333333", foreground="#ffffff", 
                                        font=("Arial", 10), borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
analysis_text.pack(fill=tk.BOTH, expand=True)
analysis_text.insert(tk.END, "📊 DETAILED ANALYSIS:\n\n", "heading")
analysis_text.insert(tk.END, "Upload a photo to see facial analysis results.")
analysis_text.config(state=tk.DISABLED)

# Suggestions
suggestions_frame = ttk.Frame(right_panel)
suggestions_frame.pack(fill=tk.BOTH, expand=True , pady=(0, 10))

suggestions_text = scrolledtext.ScrolledText(suggestions_frame, wrap=tk.WORD, bg="#333333", foreground="#ffffff", 
                                           font=("Arial", 10), borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
suggestions_text.pack(fill=tk.BOTH, expand=True)
suggestions_text.insert(tk.END, "💡 IMPROVEMENT SUGGESTIONS:\n\n", "heading")
suggestions_text.insert(tk.END, "Upload a photo to see personalized suggestions.")
suggestions_text.config(state=tk.DISABLED)

# Add text tags
analysis_text.tag_configure("heading", font=("Arial", 12, "bold"), foreground="#4CAF50")
analysis_text.tag_configure("subheading", font=("Arial", 10, "bold"), foreground="#03A9F4")
analysis_text.tag_configure("data", font=("Arial", 10), foreground="white")
analysis_text.tag_configure("good", font=("Arial", 10, "bold"), foreground="#4CAF50")
analysis_text.tag_configure("average", font=("Arial", 10, "bold"), foreground="#FFC107")
analysis_text.tag_configure("poor", font=("Arial", 10, "bold"), foreground="#F44336")

suggestions_text.tag_configure("heading", font=("Arial", 12, "bold"), foreground="#4CAF50")
suggestions_text.tag_configure("suggestion", font=("Arial", 10), foreground="white")

# ========== FOOTER ==========
footer_frame = ttk.Frame(app)
footer_frame.pack(fill=tk.X, padx=20, pady=10)

copyright_label = ttk.Label(footer_frame, text="© 2023 Phiora. All rights reserved.", style='Status.TLabel')
copyright_label.pack(side=tk.LEFT)

version_label = ttk.Label(footer_frame, text="v2.0.0", style='Status.TLabel')
version_label.pack(side=tk.RIGHT)

# ========== MAIN LOOP ==========
if __name__ == "__main__":
    app.mainloop()