from rest_framework import viewsets, mixins, generics


class GetAuthorSubViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    ViewSet для получения списка подписчиков и на кого подписан автор.
    Поддерживает метод GET и позволяет получить список подписчиков и
    на кого подписан автор.
    """
    pass


class CreateAndDectroyViewSet(generics.DestroyAPIView,
                              mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """
    ViewSet для создания и удаления объектов.
    Поддерживает методы POST и DELETE.
    """
    pass
