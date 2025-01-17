from enum import Enum
import numpy as np

from skellymodels.experimental.model_redo.models.aspect import Aspect
from skellymodels.experimental.model_redo.managers.actor import Actor
from skellymodels.experimental.model_redo.managers.anatomical_structure_factory import create_anatomical_structure_factory

from dataclasses import dataclass

from skellymodels.experimental.model_redo.utils.create_mediapipe_actor import split_data
class HumanAspectNames(Enum):
    BODY = "body"
    FACE = "face"
    LEFT_HAND = "left_hand"
    RIGHT_HAND = "right_hand"

@dataclass
class HumanConfiguration:
    include_face: bool = True
    include_hands: bool = True
    tracker_type: str = "mediapipe"

class Human(Actor):
    def __init__(self, name: str, configuration: HumanConfiguration):
        super().__init__(name)
        self.config = configuration

        self.structures = create_anatomical_structure_factory(self.config.tracker_type).create_structures()
        
        self._initialize_aspects()

    def _initialize_aspects(self):
        self._add_body()

        if self.config.include_face:
            self._add_face()

        if self.config.include_hands:
            self._add_left_hand()
            self._add_right_hand()

    def _add_body(self):
        body = Aspect(name = HumanAspectNames.BODY.value)
        body.add_metadata({"tracker_type": self.config.tracker_type})
        body.add_anatomical_structure(self.structures[HumanAspectNames.BODY.value])
        self.add_aspect(body)
    
    def _add_face(self):
        face = Aspect(name = HumanAspectNames.FACE.value)
        face.add_metadata({"tracker_type": self.config.tracker_type})
        face.add_anatomical_structure(self.structures[HumanAspectNames.FACE.value])
        self.add_aspect(face)

    def _add_left_hand(self):
        left_hand = Aspect(name = HumanAspectNames.LEFT_HAND.value)
        left_hand.add_metadata({"tracker_type": self.config.tracker_type})
        left_hand.add_anatomical_structure(self.structures[HumanAspectNames.LEFT_HAND.value])
        self.add_aspect(left_hand)

    def _add_right_hand(self):
        right_hand = Aspect(name = HumanAspectNames.RIGHT_HAND.value)
        right_hand.add_metadata({"tracker_type": self.config.tracker_type})
        right_hand.add_anatomical_structure(self.structures[HumanAspectNames.RIGHT_HAND.value])
        self.add_aspect(right_hand)

    @property
    def body(self):
        return self.aspects[HumanAspectNames.BODY.value]
    @property
    def face(self):
        return self.aspects.get(HumanAspectNames.FACE.value)
    @property
    def left_hand(self):
        return self.aspects.get(HumanAspectNames.LEFT_HAND.value)
    @property
    def right_hand(self):
        return self.aspects.get(HumanAspectNames.RIGHT_HAND.value)

    def from_tracked_points_numpy(self, tracked_points_numpy_array:np.ndarray):
        data_split_by_category = split_data(tracked_points_numpy_array)

        self.body.add_tracked_points(data_split_by_category['pose_landmarks'])

        if self.config.include_face:
            self.face.add_tracked_points(data_split_by_category['face_landmarks'])
        
        if self.config.include_hands:
            self.left_hand.add_tracked_points(data_split_by_category['left_hand_landmarks'])
            self.right_hand.add_tracked_points(data_split_by_category['right_hand_landmarks'])
