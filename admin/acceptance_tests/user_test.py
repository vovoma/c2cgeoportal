import pytest
from . import clean_form
import re
from pyramid.testing import DummyRequest


@pytest.fixture(scope='class')
@pytest.mark.usefixtures("dbsession")
def insertUsersTestData(dbsession):
    from c2cgeoportal_commons.models.main import User
    from c2cgeoportal_commons.models.main import Role
    dbsession.begin_nested()
    roles = []
    for i in range(0, 4):
        roles.append(Role("secretary_" + str(i)))
        dbsession.add(roles[i])
    for i in range(0, 23):
        user = User("babar_" + str(i),
                    email='mail' + str(i),
                    role=roles[i % 4])
        dbsession.add(user)
    yield
    dbsession.rollback()


@pytest.mark.usefixtures("insertUsersTestData", "transact")
class TestUser():
    def test_view_index(self, dbsession):
        from c2cgeoportal_admin.views.users import UserViews
        info = UserViews(DummyRequest(dbsession=dbsession)).index()
        assert info['list_fields'][0][0] == 'username'
        assert info['list_fields'][1][0] == 'email'
        assert type(info['list_fields'][1][1]) == str

    def test_view_edit(self, dbsession):
        from c2cgeoportal_admin.views.users import UserViews
        req = DummyRequest(dbsession=dbsession)
        req.matchdict.update({'id': '12'})

        form = clean_form(UserViews(req).edit()['form'])

        inputs = re.findall('<input type="text" .*?>', form)
        expected0 = '<input type="text" name="username" value="babar_9" .* "/>'
        assert re.match(expected0, inputs[0]) is not None
        expected2 = '<input type="text" name="email" value="mail9" .* "/>'
        assert re.match(expected2, inputs[2]) is not None
        selects = re.findall('<select name="role_name.*?>.*</select>', form)
        assert re.match(('<select name="role_name" .*?">'
                         ' <option value="">- Select -</option>'
                         ' <option value="secretary_0">secretary_0</option>'
                         ' <option selected="selected" value="secretary_1">secretary_1</option>'
                         ' <option value="secretary_2">secretary_2</option>'
                         ' <option value="secretary_3">secretary_3</option>'
                         ' </select>'), selects[0]) is not None

    @pytest.mark.usefixtures("test_app")  # route have to be registred for HTTP_FOUND
    def test_submit_update(self, dbsession):
        from c2cgeoportal_admin.views.users import UserViews
        post = {'__formid__': 'deform',
                '_charset_': 'UTF-8',
                'formsubmit': 'formsubmit',
                'item_type': 'user',
                'id': '11',
                'username': 'new_name_withéàô',
                'email': 'new_mail',
                'role_name': 'secretary_2',
                'is_password_changed': 'false',
                '_password': 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
                'temp_password': ''}
        req = DummyRequest(dbsession=dbsession, post=post)
        req.matchdict.update({'id': '11'})
        req.matchdict.update({'table': 'user'})

        UserViews(req).save()

        from c2cgeoportal_commons.models.main import User
        user = dbsession.query(User). \
            filter(User.username == 'new_name_withéàô').\
            one_or_none()
        assert user.email == 'new_mail'
        from c2cgeoportal_commons.models.main import Role
        role = dbsession.query(Role). \
            filter(Role.name == 'secretary_2'). \
            one_or_none()
        assert user.role == role

    @pytest.mark.usefixtures("raise_db_error_on_query")
    def test_grid_dberror(self, dbsession):
        from c2cgeoportal_admin.views.users import UserViews
        request = DummyRequest(dbsession=dbsession,
                               params={'current': 0, 'rowCount': 10})
        info = UserViews(request).grid()
        assert info.status_int == 500, '500 status when db error'

    @pytest.mark.usefixtures("test_app")
    def test_view_index_rendering_in_app(self, dbsession, test_app):
        res = test_app.get('/user/', status=200)
        res1 = res.click(verbose=True, href='language=en')
        res2 = res1.follow()
        expected = ('[<th data-column-id="username">username</th>,'
                    ' <th data-column-id="email">email</th>,'
                    ' <th data-column-id="_id_"'
                    ' data-converter="commands"'
                    ' data-searchable="false"'
                    ' data-sortable="false">Commands</th>]')
        assert expected == str(res2.html.find_all('th', limit=3))
        assert 1 == len(list(filter(lambda x: str(x.contents) == "['New']",
                                    res2.html.findAll('a'))))

    @pytest.mark.skip(reason="Translation is not finished")
    @pytest.mark.usefixtures("test_app")
    def test_view_index_rendering_in_app_fr(self, dbsession, test_app):
        res = test_app.get('/user/', status=200)
        res1 = res.click(verbose=True, href='language=fr')
        res2 = res1.follow()
        expected = ('[<th data-column-id="username">username</th>,'
                    ' <th data-column-id="email">mel</th>,'
                    ' <th data-column-id="_id_"'
                    ' data-converter="commands"'
                    ' data-searchable="false"'
                    ' data-sortable="false">Actions</th>]')
        assert expected == str(res2.html.find_all('th', limit=3))
        assert 1 == len(list(filter(lambda x: str(x.contents) == "['Nouveau']",
                                    res2.html.findAll('a'))))

    # in order to make this work, had to install selenium gecko driver
    @pytest.mark.usefixtures("selenium", "selenium_app")
    def test_selenium(self, dbsession, selenium):
        selenium.get('http://127.0.0.1:6543' + '/user/')
        # elem = selenium.find_element_by_xpath("//a[contains(@href,'language=fr')]")
        # elem.click()

        elem = selenium.find_element_by_xpath("//button[@title='Refresh']/following-sibling::*")
        elem.click()
        elem = selenium.find_element_by_xpath("//a[contains(@href,'#50')]")
        elem.click()
        elem = selenium.find_element_by_xpath("//a[contains(@href,'13/edit')]")
        elem.click()
        elem = selenium.find_element_by_xpath("//input[@name ='username']")
        elem.clear()
        elem.send_keys('new_name_éôù')
        elem = selenium.find_element_by_xpath("//input[@name ='email']")
        elem.clear()
        elem.send_keys('new_email')

        elem = selenium.find_element_by_xpath("//button[@name='formsubmit']")
        elem.click()

        from c2cgeoportal_commons.models.main import User
        user = dbsession.query(User). \
            filter(User.username == 'new_name_éôù'). \
            one_or_none()
        assert user.email == 'new_email'