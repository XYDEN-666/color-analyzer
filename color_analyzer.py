from PIL import Image, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
from colorthief import ColorThief
import webcolors
import colorsys
import requests
from io import BytesIO
import os
import base64

class ImageColorAnalyzer:
    def __init__(self):
        self.image = None
        self.color_thief = None
        
    def load_image(self, source, source_type='file'):
        try:
            if source_type == 'file':
                if not os.path.exists(source):
                    raise FileNotFoundError(f"Image file not found: {source}")
                self.image = Image.open(source)
                self._create_color_thief(source)
            else:
                raise ValueError(f"Unsupported source_type: {source_type}")
            
            self._validate_image()
            
        except Exception as e:
            raise Exception(f"Error loading image: {str(e)}")
    
    def _validate_image(self):
        if not self.image:
            raise ValueError("No image loaded")
            
        if self.image.mode not in ('RGB', 'RGBA'):
            self.image = self.image.convert('RGB')
    
    def _create_color_thief(self, source):
        if isinstance(source, (str, BytesIO)):
            self.color_thief = ColorThief(source)
        else:
            raise ValueError("Invalid source for ColorThief")
    
    def get_dominant_palette(self, color_count=5):
        """Extract dominant colors from the image."""
        palette = self.color_thief.get_palette(color_count=color_count, quality=10)
        return [self._rgb_to_hex(color) for color in palette]
    
    def suggest_palette_improvements(self):
        """Suggest improvements to the current color palette."""
        dominant_colors = self.get_dominant_palette()
        suggestions = []
        
        # Convert hex to RGB for base color
        base_rgb = webcolors.hex_to_rgb(dominant_colors[0])
        
        # Convert RGB to HSV
        h, s, v = colorsys.rgb_to_hsv(base_rgb[0]/255, base_rgb[1]/255, base_rgb[2]/255)
        
        # Generate complementary color (opposite hue)
        comp_h = (h + 0.5) % 1.0
        comp_rgb = colorsys.hsv_to_rgb(comp_h, s, v)
        comp_hex = self._rgb_to_hex([int(x * 255) for x in comp_rgb])
        
        # Generate analogous colors (nearby hues)
        analog1 = colorsys.hsv_to_rgb((h + 0.083) % 1, s, v)
        analog2 = colorsys.hsv_to_rgb((h - 0.083) % 1, s, v)
        
        suggestions.append({
            'type': 'Complementary',
            'colors': [dominant_colors[0], comp_hex],
            'description': 'Consider using this complementary color for accent elements'
        })
        
        suggestions.append({
            'type': 'Analogous',
            'colors': [
                dominant_colors[0],
                self._rgb_to_hex([int(x * 255) for x in analog1]),
                self._rgb_to_hex([int(x * 255) for x in analog2])
            ],
            'description': 'These analogous colors could create a more harmonious feel'
        })
        
        # Analyze contrast
        if len(dominant_colors) >= 2:
            contrast_ratio = self._calculate_contrast_ratio(dominant_colors[0], dominant_colors[1])
            if contrast_ratio < 4.5:
                suggestions.append({
                    'type': 'Contrast',
                    'description': f'Current contrast ratio ({contrast_ratio:.2f}) might be too low. Consider increasing contrast for better readability.'
                })
        
        return suggestions
    
    def suggest_font_colors(self, background_color):
        """Suggest font colors that work well with the given background color."""
        suggestions = []
        
        # Convert hex to RGB
        bg_rgb = webcolors.hex_to_rgb(background_color)
        
        # Calculate luminance to determine if background is light or dark
        luminance = self._get_luminance(bg_rgb)
        
        if luminance > 0.5:
            # Light background - suggest dark text
            suggestions.extend([
                {'color': '#000000', 'name': 'Black', 'contrast': self._calculate_contrast_ratio(background_color, '#000000')},
                {'color': '#333333', 'name': 'Dark Gray', 'contrast': self._calculate_contrast_ratio(background_color, '#333333')},
                {'color': '#555555', 'name': 'Medium Gray', 'contrast': self._calculate_contrast_ratio(background_color, '#555555')},
            ])
        else:
            # Dark background - suggest light text
            suggestions.extend([
                {'color': '#ffffff', 'name': 'White', 'contrast': self._calculate_contrast_ratio(background_color, '#ffffff')},
                {'color': '#f0f0f0', 'name': 'Light Gray', 'contrast': self._calculate_contrast_ratio(background_color, '#f0f0f0')},
                {'color': '#cccccc', 'name': 'Medium Light Gray', 'contrast': self._calculate_contrast_ratio(background_color, '#cccccc')},
            ])
        
        # Sort by contrast ratio (highest first)
        suggestions.sort(key=lambda x: x['contrast'], reverse=True)
        
        return suggestions
    
    def _get_luminance(self, rgb):
        """Calculate relative luminance of an RGB color."""
        rgb = np.array(rgb) / 255.0
        rgb = np.where(rgb <= 0.03928, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
        return np.dot(rgb, [0.2126, 0.7152, 0.0722])
    
    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color code."""
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def _calculate_contrast_ratio(self, color1, color2):
        """Calculate contrast ratio between two colors."""
        # Convert hex to RGB
        rgb1 = np.array(webcolors.hex_to_rgb(color1))
        rgb2 = np.array(webcolors.hex_to_rgb(color2))
        
        # Calculate relative luminance
        l1 = self._get_luminance(rgb1)
        l2 = self._get_luminance(rgb2)
        
        # Calculate contrast ratio
        ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
        return ratio

def analyze_image(source, source_type='file'):
    """Main function to analyze an image and provide color recommendations."""
    analyzer = ImageColorAnalyzer()
    analyzer.load_image(source, source_type)
    
    results = {
        'dominant_palette': analyzer.get_dominant_palette(),
        'palette_improvements': analyzer.suggest_palette_improvements(),
        'font_suggestions': analyzer.suggest_font_colors(analyzer.get_dominant_palette()[0])
    }
    
    return results