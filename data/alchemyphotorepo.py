from data.photorepo import PhotoRepo


class AlchemyPhotoRepo(PhotoRepo):

    def __init__(self, context):
        super().__init__(context)

    def get_photo(self, photo_id):
        pass

    def create_photo(self, uri):
        pass
