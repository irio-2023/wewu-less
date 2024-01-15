from marshmallow import Schema, fields, validate

from wewu_less.models.geo_region import GeoRegion

possible_regions = [r.value for r in GeoRegion]


class DeleteServiceRequestSchema(Schema):
    job_id = fields.UUID(data_key="jobId", required=True)
    geo_regions = fields.List(
        cls_or_instance=fields.Str(validate=validate.OneOf(possible_regions)),
        required=True,
        data_key="geoRegions",
    )
