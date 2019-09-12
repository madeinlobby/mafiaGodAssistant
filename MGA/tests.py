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
        kill = Buff.objects.create(duration=Duration.always, type=BuffType.Kill, priority=6, announce=True,
                                   function_name='kill')
        save = Buff.objects.create(duration=Duration.H24, type=BuffType.Save, priority=7, announce=False)
        save_at_night = Buff.objects.create(duration=Duration.always, type=BuffType.Save_at_night, priority=2,
                                            announce=False)
        save_at_night.save()
        one_shot_alive = Buff.objects.create(duration=Duration.always, type=BuffType.One_shot_alive, priority=8,
                                             announce=False)
        jailBuff = Buff.objects.create(duration=Duration.H24, type=BuffType.NotChange_announce, priority=1,
                                       announce=True)
        aman = Buff.objects.create(duration=Duration.H24, type=BuffType.NotChange, priority=1, announce=False)
        silent = Buff.objects.create(duration=Duration.H24, type=BuffType.Silent, priority=13, announce=True)
        silent.save()
        kill.neutralizer.add(save)
        kill.neutralizer.add(one_shot_alive)
        one_shot_alive.neutralizer.add(kill)
        save.neutralizer.add(kill)
        save.save()
        one_shot_alive.save()
        kill.save()

        reverse_dead = Buff.objects.create(duration=Duration.always, type=BuffType.Reverse_kill, priority=5,
                                           announce=False)
        reverse_dead.save()

        one_shot = Buff.objects.create(duration=Duration.always, type=BuffType.One_shot, priority=6,
                                       announce=True)
        one_shot.save()

        reverse_simin = Buff.objects.create(duration=Duration.H24, type=BuffType.Reverse_inquiry_simin, priority=11,
                                            announce=False)
        reverse_simin.save()

        send_role = Buff.objects.create(duration=Duration.always, type=BuffType.SendRole, priority=3, announce=False,
                                        function_name='send_role')
        send_role.save()

        make_citizen = Buff.objects.create(duration=Duration.always, type=BuffType.Make_citizen, priority=4,
                                           announce=True,
                                           function_name='make_citizen')
        make_citizen.save()

        make_alive = Buff.objects.create(duration=Duration.H12, type=BuffType.Make_alive, priority=9,
                                         announce=True,
                                         function_name='make_alive')
        make_alive.save()

        jalab_buff = Buff.objects.create(duration=Duration.H24, type=BuffType.Can_not_vote, priority=12,
                                         announce=True)
        jalab_buff.save()

        not_know_role_buff = Buff.objects.create(duration=Duration.always, type=BuffType.can_not_know_role, priority=10,
                                                 announce=False)
        not_know_role_buff.save()

        reverse_detective_buff = Buff.objects.create(duration=Duration.always, type=BuffType.Reverse_inquiry_detective,
                                                     priority=11,
                                                     announce=False)
        reverse_detective_buff.save()

        make_mafia_buff = Buff.objects.create(duration=Duration.always, type=BuffType.Make_simple_mafia,
                                              priority=1, announce=False)
        make_mafia_buff.save()

        mirror_buff = Buff.objects.create(duration=Duration.H24, type=BuffType.mirror,
                                          priority=0.5, announce=False)
        mirror_buff.save()

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

        reverse_kill_Ability = Ability.objects.create(name=AbilityEnum.reverse_kill)
        reverse_kill_Ability.buffs.add(reverse_dead)
        reverse_kill_Ability.save()

        silentAbility = Ability.objects.create(name=AbilityEnum.can_silence)
        silentAbility.buffs.add(silent)
        saveAbility.save()

        can_not_know_role_Ability = Ability.objects.create(name=AbilityEnum.can_not_know_role)
        can_not_know_role_Ability.buffs.add(not_know_role_buff)
        can_not_know_role_Ability.save()

        mirror_Ability = Ability.objects.create(name=AbilityEnum.mirror)
        mirror_Ability.buffs.add(mirror_buff)
        mirror_Ability.save()

        revers_inquiry = Ability.objects.create(name=AbilityEnum.reverse_inquiry_detective)
        revers_inquiry.buffs.add(reverse_detective_buff)
        revers_inquiry.save()

        send_role_abiity = Ability.objects.create(name=AbilityEnum.can_send_role)
        send_role_abiity.buffs.add(send_role)
        send_role_abiity.save()

        jalab_abiity = Ability.objects.create(name=AbilityEnum.can_not_vote)
        jalab_abiity.buffs.add(jalab_buff)
        jalab_abiity.save()

        one_shot_ability = Ability.objects.create(name=AbilityEnum.one_shot)
        one_shot_ability.buffs.add(one_shot)
        one_shot_ability.save()

        save_at_night_ability = Ability.objects.create(name=AbilityEnum.can_save_at_night)
        save_at_night_ability.buffs.add(save_at_night)
        save_at_night_ability.save()

        make_citizen_ability = Ability.objects.create(name=AbilityEnum.can_change_role_to_citizen)
        make_citizen_ability.buffs.add(make_citizen)
        make_citizen_ability.save()

        make_alive_ability = Ability.objects.create(name=AbilityEnum.can_alive)
        make_alive_ability.buffs.add(make_alive)
        make_alive_ability.save()

        make_mafia_ability = Ability.objects.create(name=AbilityEnum.make_simple_mafia)
        make_mafia_ability.buffs.add(make_mafia_buff)
        make_mafia_ability.save()

        one_shot_ability = Ability.objects.create(name=AbilityEnum.one_shot_alive)
        one_shot_ability.buffs.add(one_shot_alive)
        one_shot_ability.save()

        reverse_simin_ability = Ability.objects.create(name=AbilityEnum.reverse_inquiry_simin)
        reverse_simin_ability.buffs.add(reverse_simin)
        reverse_simin_ability.save()

        Role.objects.create(name=RoleEnum.citizen, team=TeamEnum.citizen, wake_up=WakeUpEnum.never).save()
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
        wolfman.own_buffs.add(reverse_dead)
        wolfman.save()

        simin = Role.objects.create(name=RoleEnum.simin, team=TeamEnum.citizen,
                                    wake_up=WakeUpEnum.every_night)
        simin.abilities.add(can_ask)
        simin.save()

        priest = Role.objects.create(name=RoleEnum.priest, team=TeamEnum.citizen,
                                     wake_up=WakeUpEnum.every_three_night)
        priest.abilities.add(make_citizen_ability)
        priest.own_buffs.add(one_shot_alive)
        priest.save()

        grave_digger = Role.objects.create(name=RoleEnum.grave_digger, team=TeamEnum.citizen, limit=2,
                                           wake_up=WakeUpEnum.every_night)
        grave_digger.abilities.add(can_ask)
        grave_digger.save()

        insincere = Role.objects.create(name=RoleEnum.insincere, team=TeamEnum.mafia,
                                        wake_up=WakeUpEnum.every_night)
        insincere.own_buffs.add(revers_inquiry)
        insincere.save()

        jesus = Role.objects.create(name=RoleEnum.jesus, team=TeamEnum.citizen,
                                    wake_up=WakeUpEnum.every_five_night)
        jesus.abilities.add(make_alive_ability)
        jesus.save()

        mafia_boss = Role.objects.create(name=RoleEnum.don, team=TeamEnum.mafia,
                                         wake_up=WakeUpEnum.every_night)
        mafia_boss.abilities.add(revers_inquiry)
        mafia_boss.save()

        half_breed = Role.objects.create(name=RoleEnum.half_breed, team=TeamEnum.werewolf,
                                         wake_up=WakeUpEnum.every_night)
        half_breed.abilities.add(reverse_simin_ability)
        half_breed.own_buffs.add(reverse_dead)
        half_breed.save()

        jalab = Role.objects.create(name=RoleEnum.snide, team=TeamEnum.mafia,
                                    wake_up=WakeUpEnum.every_night, limit=1)
        jalab.abilities.add(jalab_abiity)
        jalab.save()

        jani = Role.objects.create(name=RoleEnum.criminal, team=TeamEnum.criminals,
                                   wake_up=WakeUpEnum.every_two_night)
        jani.abilities.add(killAbility)
        jani.save()

        chalkon = Role.objects.create(name=RoleEnum.burial, team=TeamEnum.mafia,
                                      wake_up=WakeUpEnum.every_night, limit=2)
        chalkon.abilities.add(can_not_know_role_Ability)
        chalkon.save()

        charlatan = Role.objects.create(name=RoleEnum.charlatan, team=TeamEnum.mafia,
                                        wake_up=WakeUpEnum.every_night)
        charlatan.abilities.add(revers_inquiry)
        charlatan.save()

        killer = Role.objects.create(name=RoleEnum.killer, team=TeamEnum.mafia
                                     , wake_up=WakeUpEnum.never)
        killer.abilities.add(killAbility)
        killer.save()

        ravankav = Role.objects.create(name=RoleEnum.psychoanalyst, team=TeamEnum.mafia
                                       , wake_up=WakeUpEnum.every_night, limit=1)
        ravankav.abilities.add(make_mafia_ability)
        ravankav.save()

        night_slept = Role.objects.create(name=RoleEnum.night_slept, team=TeamEnum.mafia
                                          , wake_up=WakeUpEnum.every_night)
        night_slept.abilities.add(mirror_Ability)
        night_slept.save()

        self.assertEqual(kill.neutralizer.count(), 2)

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

    def test_sixteen(self):
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
        self.fill_member('haniye', 16)
        self.fill_member('we', 17)

        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')

        dic = {1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
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

        dic = {'زندانبان': 'kari', 'مافیا': 'zari', 'دکتر': 'karim', 'جراح': 'ali',
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

    def test_priest(self):
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
        self.fill_member('haniye', 16)

        url = reverse('logic:create_game')
        data = {'event_id': 1}
        self.client.post(url, data, format='json')
        dic = {1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1}
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
        game = Game.objects.get(id=1)
        players = game.player_set
        killshe = 'zara'
        for player in players.all():
            if player.role.name == str(RoleEnum.priest.value):
                killshe = player.user.username
                break

        print()
        print('keshiiiiiiiiiiiiiiiiiiiiiiish')
        print(killshe)

        dic = {'زندانبان': 'kari', 'مافیا': killshe, 'دکتر': killshe, 'جراح': 'ali',
               'دندان پزشک': 'bari'}
        self.set_game_aim(dic)
        self.test_night_to_day()

        print('-------------------------------')

        self.test_day_to_night()
        dic = {'مافیا': killshe, 'دکتر': 'mari', 'کارآگاه': 'zari', 'زندانبان': '', 'دندان پزشک': ''}
        self.set_game_aim(dic)
        self.test_night_to_day()

        print('---------------------------------')

        self.test_day_to_night()
        dic = {'زندانبان': '', 'قهرمان': 'ali', 'مافیا': 'mari', 'دکتر': 'qari', 'جراح': 'ali',
               'دندان پزشک': ''}
        self.set_game_aim(dic)

        url = reverse('logic:ask_god')
        data = {'game_id': 1, 'role_name': 'کارآگاه', 'player_username': 'zahra'}
        response = self.client.post(url, data, format='json')
        print(response.data)
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
        self.test_set_game_role_true()

