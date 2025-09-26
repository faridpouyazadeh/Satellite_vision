import supervision as sv
import cv2
from ultralytics import YOLOWorld, YOLO
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


class Model:
    def __init__(self):
        self.base_model_path = "structure_folder/Model.pt"
        self.upgraded_model_path = "structure_folder/models_folder/Upgraded_Model.pt"
        os.makedirs("structure_folder/models_folder", exist_ok=True)
        os.makedirs("structure_folder/CSV_folder", exist_ok=True)
        os.makedirs("structure_folder/video_tracked", exist_ok=True)
    
    def _get_model(self):
        """Get the best available model"""
        if os.path.exists(self.upgraded_model_path):
            return YOLOWorld(self.upgraded_model_path)
        return YOLOWorld(self.base_model_path)
    
    def _validate_image_path(self, img_path):
        """Validate image path"""
        if not img_path or '..' in img_path or not os.path.exists(img_path):
            return False
        return True
    
    def _process_image(self, model, img_path):
        """Common image processing logic"""
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
        
        box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        annotated_image = box_annotator.annotate(scene=image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
        
        display.display(annotated_image)
        return "Done"
    
    def _track_video(self, model, video_path):
        """Common video tracking logic"""
        frames_generator = sv.get_video_frames_generator(video_path)
        
        with sv.CSVSink("structure_folder/CSV_folder/Output_Track_on_Video.csv") as sink:
            for frame in frames_generator:
                results = model(frame)[0]
                detections = sv.Detections.from_ultralytics(results)
                sink.append(detections, {})
        
        print("CSV-File saved in <structure_folder/CSV_folder/Output_Track_on_Video.csv>")
        
        tracker = sv.ByteTrack()
        box_annotator = sv.BoxAnnotator()
        
        def callback(frame: np.ndarray, _: int) -> np.ndarray:
            results = model(frame)[0]
            detections = sv.Detections.from_ultralytics(results)
            detections = tracker.update_with_detections(detections)
            return box_annotator.annotate(frame.copy(), detections=detections)
        
        sv.process_video(
            source_path=video_path,
            target_path="structure_folder/video_tracked/result.mp4",
            callback=callback
        )
        print("Video saved in <structure_folder/video_tracked/result.mp4>")
        return "Done"

    def train(self, yaml_file_train):
        """Train the model"""
        try:
            if not yaml_file_train or not os.path.exists(yaml_file_train):
                raise ValueError("Invalid YAML file path")
            
            model = YOLOWorld(self.base_model_path)
            results = model.train(data=yaml_file_train, epochs=100, imgsz=640)
            
            if not results:
                raise RuntimeError("Training failed")
            
            model.save(self.upgraded_model_path)
            print(f"Model saved in <{self.upgraded_model_path}>")
            return "Done"
            
        except Exception as e:
            print(f"Training error: {e}")
            return ""

    def predict(self, img_path):
        """Predict objects in image"""
        try:
            model = self._get_model()
            return self._process_image(model, img_path)
        except Exception as e:
            print(f"Prediction error: {e}")
            return ""

    def validation(self, yaml_file_val):
        """Validate the model"""
        try:
            if not yaml_file_val or not os.path.exists(yaml_file_val):
                raise ValueError("Invalid YAML file path")
            
            model = YOLO(self.upgraded_model_path if os.path.exists(self.upgraded_model_path) else self.base_model_path)
            metrics = model.val(data=yaml_file_val, plots=True)
            print(metrics.confusion_matrix.to_df())
            return "Done"
            
        except Exception as e:
            print(f"Validation error: {e}")
            return ""

    def track(self, video_path):
        """Track objects in video"""
        try:
            if not video_path or not os.path.exists(video_path):
                raise ValueError("Invalid video path")
            
            model = YOLO(self.upgraded_model_path if os.path.exists(self.upgraded_model_path) else self.base_model_path)
            return self._track_video(model, video_path)
            
        except Exception as e:
            print(f"Tracking error: {e}")
            return ""

    def define_custom_classes(self, img_path, order_class):
        """Define custom classes for detection"""
        try:
            model = self._get_model()
            model.set_classes(order_class)
            return self._process_image(model, img_path)
            
        except Exception as e:
            print(f"Custom classes error: {e}")
            return ""

    def save_define_model(self, order_class):
        """Save model with custom classes"""
        try:
            model = self._get_model()
            model.set_classes(order_class)
            
            save_path = (self.upgraded_model_path.replace('.pt', '_Defined.pt') 
                        if os.path.exists(self.upgraded_model_path) 
                        else self.base_model_path.replace('.pt', '_Defined.pt'))
            
            model.save(save_path)
            print(f"Defined model saved in <{save_path}>")
            return "Done"
            
        except Exception as e:
            print(f"Save model error: {e}")
            return ""