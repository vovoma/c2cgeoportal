from pyramid.view import view_defaults
from pyramid.view import view_config
from c2cgeoform.views.abstract_views import AbstractViews
from c2cgeoportal_commons.models.main import Role
from colanderalchemy import setup_schema

setup_schema(None, Role)


@view_defaults(match_param='table=role')
class RoleViews(AbstractViews):
    _list_fields = ['name']
    _id_field = 'id'
    _model = Role
    _base_schema = Role.__colanderalchemy__

    @view_config(route_name='c2cgeoform_index',
                 renderer="c2cgeoform:templates/site/index.pt")
    def index(self):
        return super().index()

    @view_config(route_name='c2cgeoform_grid',
                 renderer="json")
    def grid(self):
        return super().grid()

    @view_config(route_name='c2cgeoform_action',
                 request_method='GET',
                 renderer="c2cgeoform:templates/site/edit.pt")
    def view(self):
        return super().edit()

    @view_config(route_name='c2cgeoform_action',
                 request_method='POST',
                 renderer="c2cgeoform:templates/site/edit.pt")
    def save(self):
        return super().save()