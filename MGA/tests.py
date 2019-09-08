from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from MGA.models import User, Event
from logic.models import Role, Buff, Duration, BuffType, RoleEnum, Ability, AbilityEnum, TeamEnum, Player
from mafiaGodAssistant import settings


class Tests(APITestCase):
    def test_login_user(self):
        """
        Ensure login is ok!
        """
        self.test_create_user()  # make ctest in default db
        url = reverse('login')
        data = {'username': "ctest", 'password': "ctest12345"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Ensure signup is ok!
        """
        url = reverse('signup')
        data = {'username': 'ctest', 'name': 'name', 'password': 'ctest12345', 'bio': 'bio',
                'phoneNumber': '9382593895', 'city': 'tehran', 'email': 'z.y.j.1379@gmail.com', 'device': 'android'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_user(self, username):
        """
        Ensure signup is ok!
        """
        url = reverse('signup')
        data = {'username': username, 'name': 'name', 'password': 'ctest12345', 'bio': 'bio',
                'phoneNumber': '9382593895', 'city': 'tehran', 'email': 'z.y.j.1379@gmail.com', 'device': 'android'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logout_user(self):
        """
        Ensure logout is ok!
        """
        self.test_login_user()
        url = reverse('logout')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        """
        Ensure changing password is ok!
        """
        self.test_login_user()
        url = reverse('change_password')
        data = {'oldPassword': "ctest12345", 'newPassword': 'test12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        """
        Ensure reset password is ok!
        """
        self.test_create_user()
        url = reverse('reset_password')
        data = {'id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_friend(self):
        """
        Ensure friend request is ok!
        """
        self.test_login_user()
        self.test_create_user('b')
        url = reverse('MGA:send_friend_request')
        data = {'id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_friend(self):
        """
        Ensure friend request is ok!
        """
        self.test_request_friend()
        url = reverse('MGA:accept_friend_request')
        data = {'id': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization(self):
        """
        Ensure create org is ok!
        """
        self.test_login_user()
        url = reverse('MGA:create_organization')
        data = {'name': "event"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_admin(self):
        """
        Ensure add admin is ok!
        """
        self.test_create_user()
        self.test_create_organization()
        url = reverse('MGA:add_admin')
        data = {'admin id': 1, 'org_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_event(self):
        """
        Ensure create event is ok!
        """
        self.test_create_organization()
        url = reverse('MGA:add_event')
        data = {'org_id': 1, 'title': 'first', 'capacity': 5, 'description': 'nothing!', 'date': now()}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def fill_member(self, name, id):
        self.create_user(name)
        url = reverse('MGA:add_member')
        print(self.client.post(url, {'user_id': id, 'event_id': 1}, format='json').status_code)

    def test_create_cafe(self):
        url = reverse('MGA:create_cafe')
        data = {'name': 'cafe', 'phoneNumber': '123456', 'telephone': '1234', 'capacity': 34, 'description': 'asdf',
                'forbiddens': "nothing!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_message(self):
        url = reverse('signup')
        data = {'username': 'mut', 'name': 'nme', 'password': 'ctest12345', 'bio': 'bio',
                'phoneNumber': '9382593895', 'city': 'tehran', 'email': 'z.j.1379@gmail.com', 'device': 'android'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_login_user()
        url = reverse('chat:send_to_one')
        data = {'text': 'hello', 'receiver_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_group(self):
        self.test_login_user()
        url = reverse('chat:create_group')
        data = {'name': 'gruop'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_message_to_group(self):
        self.test_create_group()
        url = reverse('chat:send_to_group')
        data = {'group_id': 1, 'text': 'hello'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_group(self):
        self.test_create_group()
        url = reverse('chat:delete_group', args=[1])
        data = {'id': 1}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_message(self):
        self.test_create_message()
        url = reverse('chat:edit_message')
        data = {'message_id': 1, 'new_text': 'hello'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message(self):
        self.test_edit_message()
        url = reverse('chat:get_message', args=[1])
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_game(self):
        self.test_add_event()
        url = reverse('logic:create_game')
        data = {'event_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_roles(self):
        Role.objects.create(name='شهروند عادی').save()
        Role.objects.create(name='دکتر').save()
        Role.objects.create(name='کارآگاه').save()
        Role.objects.create(name='مافیا').save()
        url = reverse('logic:get_all_roles')
        data = {}
        response = self.client.get(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_game_role_false(self):
        self.test_create_game()
        self.test_get_all_roles()
        dic = {1: 1, 2: 1, 3: 1, 4: 1}
        url = reverse('logic:set_game_role')
        data = {'game_id': 1, 'role_dict': dic}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_game_role_true(self):
        self.test_fill_member()
        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')
        self.test_get_all_roles()
        dic = {1: 1, 2: 1, 3: 1, 4: 1}
        url = reverse('logic:set_game_role')
        data = {'game_id': 1, 'role_dict': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_init(self):
        kill = Buff.objects.create(duration=Duration.always, type=BuffType.Kill, priority=3, announce=True,
                                   function_name='kill')
        save = Buff.objects.create(duration=Duration.H12, type=BuffType.Save, priority=3, announce=False)
        jail_save = Buff.objects.create(duration=Duration.H24, type=BuffType.Save, priority=3, announce=True)
        kill.neutralizer.add(save, jail_save)
        save.neutralizer.add(kill)
        jail_save.neutralizer.add(kill)

        Ability.objects.create(name=AbilityEnum.can_ask).save()
        killAbility = Ability.objects.create(name=AbilityEnum.can_kil)
        killAbility.buffs.add(kill)
        kill.save()
        saveAbility = Ability.objects.create(name=AbilityEnum.can_save)
        saveAbility.buffs.add(save)
        saveAbility.save()

        Role.objects.create(name=RoleEnum.citizen, team=TeamEnum.citizen).save()
        doctor = Role.objects.create(name=RoleEnum.doctor, team=TeamEnum.citizen)
        detective = Role.objects.create(name=RoleEnum.detective, team=TeamEnum.citizen)
        mafia = Role.objects.create(name=RoleEnum.mafia, team=TeamEnum.mafia)
        doctor.abilities.add(Ability.objects.get(id=3))
        detective.abilities.add(Ability.objects.get(id=1))
        mafia.abilities.add(Ability.objects.get(id=2))
        doctor.save()
        detective.save()
        mafia.save()
        jailer = Role.objects.create(name=RoleEnum.jailer, team=TeamEnum.citizen)
        jailer.abilities.add()
        self.assertEqual(kill.neutralizer.count(), 2)

    def test_four(self):
        self.test_init()
        self.test_add_event()
        self.fill_member('zari', 2)
        self.fill_member('kari', 3)
        self.fill_member('mari', 4)
        self.fill_member('qari',5)

        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')
        dic = {1: 1, 2: 1, 3: 1, 4: 1, 5: 0}
        url = reverse('logic:set_game_role')
        data = {'game_id': 1, 'role_dict': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_start_game()

    def test_five(self):
        self.test_init()
        self.test_add_event()
        self.fill_member('zari', 2)
        self.fill_member('kari', 3)
        self.fill_member('mari', 4)
        self.fill_member('qari', 5)
        self.fill_member('pari',6)

        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')
        dic = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        url = reverse('logic:set_game_role')
        data = {'game_id': 1, 'role_dict': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_start_game()


    def test_start_game(self):
        url = reverse('logic:day_to_night')
        data = {'game_id': 1}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logic:set_night_aim')
        dic = {'مافیا': 'zari', 'دکتر': 'mari', 'کارآگاه': 'zari'}
        data = {'aim_dic': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logic:night_to_day')
        data = {'game_id': 1}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
