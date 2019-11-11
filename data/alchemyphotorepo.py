from data.photorepo import PhotoRepo
from models import Photo


class AlchemyPhotoRepo(PhotoRepo):

    def __init__(self, context):
        super().__init__(context)

    def create_photo(self, uri):
        photo = Photo(uri)
        self._context.get_context().add(photo)
        self._context.get_context().flush()
        self._context.get_context().refresh(photo)
        return photo

    def get_photo(self, photo_id):
        return self._context.get_context().query(Photo).filter_by(id=photo_id).first()
