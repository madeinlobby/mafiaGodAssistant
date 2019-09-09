from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from MGA.models import User, Event
from logic.models import Role, Buff, Duration, BuffType, RoleEnum, Ability, AbilityEnum, TeamEnum, Player, Game, \
    WakeUpEnum
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
        self.fill_member('zari', 2)
        self.fill_member('kari', 3)
        self.fill_member('mari', 4)
        self.fill_member('qari', 5)
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
        save_at_night = Buff.objects.create(duration=Duration.always, type=BuffType.Save_at_night, priority=3,
                                            announce=False)
        save_at_night.save()
        jailBuff = Buff.objects.create(duration=Duration.H24, type=BuffType.NotChange_announce, priority=1,
                                       announce=True)
        aman = Buff.objects.create(duration=Duration.H24, type=BuffType.NotChange, priority=1, announce=False)
        silent = Buff.objects.create(duration=Duration.H24, type=BuffType.Silent, priority=1, announce=True)
        silent.save()
        kill.neutralizer.add(save)
        save.neutralizer.add(kill)

        send_role = Buff.objects.create(duration=Duration.always, type=BuffType.SendRole, priority=1, announce=False,
                                        function_name='send_role')
        send_role.save()

        make_citizen = Buff.objects.create(duration=Duration.always, type=BuffType.Make_citizen, priority=1,
                                           announce=True,
                                           function_name='make_citizen')
        make_citizen.save()

        can_ask = Ability.objects.create(name=AbilityEnum.can_ask)
        can_ask.save()
        killAbility = Ability.objects.create(name=AbilityEnum.can_kil)
        killAbility.buffs.add(kill)
        kill.save()
        saveAbility = Ability.objects.create(name=AbilityEnum.can_save)
        saveAbility.buffs.add(save)
        saveAbility.save()

        jailAbility = Ability.objects.create(name=AbilityEnum.can_jail)
        jailAbility.buffs.add(jailBuff)
        saveAbility.save()

        heroAbility = Ability.objects.create(name=AbilityEnum.can_protect)
        heroAbility.buffs.add(aman)
        heroAbility.save()

        silentAbility = Ability.objects.create(name=AbilityEnum.can_silence)
        silentAbility.buffs.add(silent)
        saveAbility.save()

        revers_inquiry = Ability.objects.create(name=AbilityEnum.reverse_inquiry)
        revers_inquiry.save()

        send_role_abiity = Ability.objects.create(name=AbilityEnum.can_send_role)
        send_role_abiity.buffs.add(send_role)
        send_role_abiity.save()

        save_at_night_ability = Ability.objects.create(name=AbilityEnum.can_save_at_night)
        save_at_night_ability.buffs.add(save_at_night)
        save_at_night_ability.save()

        make_citizen_ability = Ability.objects.create(name=AbilityEnum.can_change_role_to_citizen)
        make_citizen_ability.buffs.add(make_citizen)
        make_citizen_ability.save()

        Role.objects.create(name=RoleEnum.citizen, team=TeamEnum.citizen, wake_up=WakeUpEnum.every_night).save()
        doctor = Role.objects.create(name=RoleEnum.doctor, team=TeamEnum.citizen, wake_up=WakeUpEnum.every_night)
        detective = Role.objects.create(name=RoleEnum.detective, team=TeamEnum.citizen, wake_up=WakeUpEnum.every_night)
        mafia = Role.objects.create(name=RoleEnum.mafia, team=TeamEnum.mafia, wake_up=WakeUpEnum.every_night)
        doctor.abilities.add(saveAbility)
        detective.abilities.add(can_ask)
        mafia.abilities.add(killAbility)
        doctor.save()
        detective.save()
        mafia.save()

        jailer = Role.objects.create(name=RoleEnum.jailer, team=TeamEnum.citizen, limit=2,
                                     wake_up=WakeUpEnum.every_night)
        jailer.abilities.add(jailAbility)
        jailer.save()

        dentist = Role.objects.create(name=RoleEnum.dentist, team=TeamEnum.citizen, limit=2,
                                      wake_up=WakeUpEnum.every_night)
        dentist.abilities.add(silentAbility)
        dentist.save()

        sergeon = Role.objects.create(name=RoleEnum.surgeon, team=TeamEnum.mafia,
                                      wake_up=WakeUpEnum.every_night)
        sergeon.abilities.add(saveAbility)
        sergeon.save()

        hero = Role.objects.create(name=RoleEnum.hero, team=TeamEnum.citizen,
                                   wake_up=WakeUpEnum.every_one_night)
        hero.abilities.add(heroAbility)
        hero.save()

        wolfman = Role.objects.create(name=RoleEnum.wolfman, team=TeamEnum.werewolf,
                                      wake_up=WakeUpEnum.every_three_night)
        wolfman.abilities.add(heroAbility)
        wolfman.abilities.add(save_at_night_ability)
        wolfman.save()

        simin = Role.objects.create(name=RoleEnum.simin, team=TeamEnum.citizen,
                                    wake_up=WakeUpEnum.every_night)
        simin.abilities.add(can_ask)
        simin.save()

        priest = Role.objects.create(name=RoleEnum.priest, team=TeamEnum.citizen,
                                     wake_up=WakeUpEnum.every_three_night)
        priest.abilities.add(make_citizen_ability)
        priest.save()

        grave_digger = Role.objects.create(name=RoleEnum.grave_digger, team=TeamEnum.citizen, limit=2,
                                           wake_up=WakeUpEnum.every_night)
        grave_digger.abilities.add(can_ask)
        grave_digger.save()

        insincere = Role.objects.create(name=RoleEnum.insincere, team=TeamEnum.mafia, limit=2,
                                           wake_up=WakeUpEnum.every_night)
        insincere.abilities.add(revers_inquiry)
        insincere.save()

        self.assertEqual(kill.neutralizer.count(), 1)

    def test_day_to_night(self):
        url = reverse('logic:day_to_night')
        data = {'game_id': 1}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_night_to_day(self):
        url = reverse('logic:night_to_day')
        data = {'game_id': 1}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def set_game_aim(self, dic):
        url = reverse('logic:set_night_aim')
        data = {'aim_dic': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_four(self):
        self.test_init()
        self.test_add_event()
        self.fill_member('zari', 2)
        self.fill_member('kari', 3)
        self.fill_member('mari', 4)
        self.fill_member('qari', 5)

        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')
        dic = {1: 1, 2: 1, 3: 1, 4: 1, 5: 0}
        url = reverse('logic:set_game_role')
        data = {'game_id': 1, 'role_dict': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_day_to_night()
        dic = {'مافیا': 'zari', 'دکتر': 'mari', 'کارآگاه': 'zari'}
        self.set_game_aim(dic)
        self.test_night_to_day()

    def test_fourteen(self):
        self.test_init()
        self.test_add_event()
        self.fill_member('zari', 2)
        self.fill_member('kari', 3)
        self.fill_member('mari', 4)
        self.fill_member('qari', 5)
        self.fill_member('pari', 6)
        self.fill_member('ali', 7)
        self.fill_member('bari', 8)
        self.fill_member('zahra', 9)
        self.fill_member('karim', 10)
        self.fill_member('baqer', 11)
        self.fill_member('saba', 12)
        self.fill_member('elnaz', 13)
        self.fill_member('rahim', 14)
        self.fill_member('javad', 15)

        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')
        dic = {1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1,13:1}
        url = reverse('logic:set_game_role')
        data = {'game_id': 1, 'role_dict': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logic:speech_for_start')
        data = {'game_id': 1}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_day_to_night()

        dic = {'زندانبان': 'kari', 'مافیا': 'zari', 'دکتر': 'mari', 'جراح': 'ali',
               'دندان پزشک': 'bari'}
        self.set_game_aim(dic)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'کارآگاه', 'player_username': 'mari'}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'سیمین', 'player_username': 'mari'}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_night_to_day()

        self.test_day_to_night()
        dic = {'زندانبان': '', 'قهرمان': 'ali', 'مافیا': 'mari', 'دکتر': 'qari', 'جراح': 'ali',
               'دندان پزشک': ''}
        self.set_game_aim(dic)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'کارآگاه', 'player_username': 'zahra'}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'گورکن', 'player_username': 'zari'}
        response = self.client.post(url, data, format='json')
        print('استعلام گورکن')
        print(response.data)
        print()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_night_to_day()

        self.test_day_to_night()
        dic = {'مافیا': 'mari', 'دکتر': 'mari', 'کارآگاه': 'zari', 'زندانبان': '', 'دندان پزشک': ''}
        self.set_game_aim(dic)
        self.test_night_to_day()

        self.test_day_to_night()
        dic = {'مافیا': 'mari', 'دکتر': 'mari', 'کارآگاه': 'zari', 'زندانبان': '', 'دندان پزشک': ''}
        self.set_game_aim(dic)
        self.test_night_to_day()

    def test_check_night(self):
        self.test_init()
        self.test_add_event()
        self.fill_member('zari', 2)
        self.fill_member('kari', 3)
        self.fill_member('mari', 4)
        self.fill_member('qari', 5)
        self.fill_member('pari', 6)
        self.fill_member('ali', 7)
        self.fill_member('bari', 8)
        self.fill_member('zahra', 9)
        self.fill_member('karim', 10)
        self.fill_member('baqer', 11)
        self.fill_member('saba', 12)

        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')
        dic = {1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}
        url = reverse('logic:set_game_role')
        data = {'game_id': 1, 'role_dict': dic}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logic:speech_for_start')
        data = {'game_id': 1}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_day_to_night()

        dic = {'زندانبان': 'kari', 'مافیا': 'zari', 'دکتر': 'mari', 'جراح': 'ali',
               'دندان پزشک': 'bari'}
        self.set_game_aim(dic)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'کارآگاه', 'player_username': 'mari'}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'سیمین', 'player_username': 'mari'}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_night_to_day()
        dic = {}
        self.test_day_to_night()
        self.set_game_aim(dic)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'کارآگاه', 'player_username': 'zahra'}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_night_to_day()

        self.test_day_to_night()
        self.set_game_aim(dic)
        self.test_night_to_day()

        self.test_day_to_night()
        self.set_game_aim(dic)
        self.test_night_to_day()
