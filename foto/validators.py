from django.core.exceptions import ValidationError


def validate_image(tipes):
    def validator(image):
        if image.format not in tipes:
            raise ValidationError(
                [f'Загрузите файл формата PNG ил JPG.']
            )
        else:
            return

    return validator