from rest_framework import serializers


# class TrackListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         duration = time.strftime('%M:%S', time.gmtime(value.duration))
#         return 'Track %d: %s (%s)' % (value.order, value.name, duration)


# class 