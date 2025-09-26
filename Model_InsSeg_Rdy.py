import supervision as sv
from ultralytics import YOLO
import cv2
import numpy as np
import os
try:
    from IPython import display
except ImportError:
    # Fallback for environments without IPython
    class MockDisplay:
        @staticmethod
        def display(image):
            print("Image processed (IPython display not available)")
    display = MockDisplay()


class Model_InsSeg:
    def __init__(self):
        self.base_model_path = "structure_folder/Model_InsSeg.pt"
        self.upgraded_model_path = "structure_folder/models_folder/Upgraded_Model_InsSeg.pt"
        os.makedirs("structure_folder/models_folder", exist_ok=True)
    
    def _get_model(self):
        """Get the best available model"""
        if os.path.exists(self.upgraded_model_path):
            return YOLO(self.upgraded_model_path)
        return YOLO(self.base_model_path)
    
    def _validate_image_path(self, img_path):
        """Validate image path to prevent path traversal"""
        if not img_path or '..' in img_path or not os.path.exists(img_path):
            return False
        return True
    
    def _process_segmentation(self, model, img_path):
        """Common segmentation processing logic"""
        if not self._validate_image_path(img_path):
            raise ValueError("Invalid image path")
        
        image = cv2.imread(img_path)
        if image is None:
            raise ValueError("Failed to load image")
        
        image = sv.resize_image(image=image, resolution_wh=(640, 640), keep_aspect_ratio=True)
        
        def callback(image_slice: np.ndarray) -> sv.Detections:
            result = model(image_slice)[0]
            return sv.Detections.from_ultralytics(result)
        
        slicer = sv.InferenceSlicer(callback=callback)
        detections = slicer(image)
        
        mask_annotator = sv.MaskAnnotator()
        label_annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER_OF_MASS)
        
        annotated_image = mask_annotator.annotate(scene=image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
        
        display.display(annotated_image)
        return "Done"

    def train(self, yaml_file):
        """Train instance segmentation model"""
        try:
            if not yaml_file or not os.path.exists(yaml_file):
                raise ValueError("Invalid YAML file path")
            
            model = YOLO(self.base_model_path)
            results = model.train(data=yaml_file, epochs=50, imgsz=640)
            
            if not results:
                raise RuntimeError("Training failed")
            
            model.save(self.upgraded_model_path)
            print(f"Model saved in <{self.upgraded_model_path}>")
            return "Done"
            
        except Exception as e:
            print(f"Training error: {e}")
            return ""

    def define_custom_classes(self, order):
        """Define custom classes for segmentation"""
        try:
            model = self._get_model()
            model.set_classes(order)
            
            save_path = (self.upgraded_model_path.replace('.pt', '_Defined.pt') 
                        if os.path.exists(self.upgraded_model_path) 
                        else self.base_model_path.replace('.pt', '_Defined.pt'))
            
            model.save(save_path)
            print(f"Model saved in <{save_path}>")
            return "Done"
            
        except Exception as e:
            print(f"Custom classes error: {e}")
            return ""

    def predict(self, img_path):
        """Predict instance segmentation"""
        try:
            model = self._get_model()
            return self._process_segmentation(model, img_path)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return ""