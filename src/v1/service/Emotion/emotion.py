class Emotion:
    """ Description of Service """

    def __init__(self, video_id: str):
        """ Description of Method """
        self.video_id = video_id

    def get(self):
        """ Description of Method """
        return f"Emotion get method result for {self.video_id}"
