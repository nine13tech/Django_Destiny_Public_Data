import json
import sqlite3
from datetime import datetime, timezone
from dateutil import parser as dateparser
from warmind_d2 import destiny2
from warmind_d2.utils import API
from Destiny_Public_Data.models import Milestones, Variants

sqlite_manifest = 'data/manifest.sqlite3'


class UpdatePublicData(object):

    def refresh_public_milestone_data(self):
        print('wo')
        api_test = self.test_api()
        if api_test != 'error':
            self.blank_databases()
            self.update_public_milestones()
        else:
            exit()

    def test_api(self):
        d2_destiny_api_instance = destiny2.Destiny2()
        api_response = d2_destiny_api_instance.get_destiny_manifest()
        if api_response.error_code != 1:
            print(api_response.error_status)
            print(api_response.message)
            exit()
        else:
            return api_response

    def blank_databases(self):
        Milestones.objects.all().delete()
        Variants.objects.all().delete()
        # exit()

    def query_table(self, table, id_hash):
        conn = sqlite3.connect(sqlite_manifest)
        cur = conn.cursor()
        api = API()
        query = 'SELECT json FROM ' + table + ' WHERE id=\'' + str(api.int32(id_hash)) + '\''
        cur.execute(query)
        this_out = cur.fetchone()
        conn.commit()
        conn.close()
        # print(this_out)
        this_json = json.loads("".join(this_out))
        return this_json

    def update_public_milestones(self):
        d2_destiny_api_instance = destiny2.Destiny2()
        api = API()
        Milestones.objects.all()

        api_response = d2_destiny_api_instance.get_public_milestones()
        print(api_response)
        # TODO: create sql schema for this mess.
        print('///')
        for each in api_response["Response"]:
            activity_json = self.query_table('DestinyMilestoneDefinition', each)
            if int(each) != 4109359897 and int(each) != 463010297 and int(each) != 383198939 and int(
                    each) != 3245985898 and int(each) != 534869653:
                print(api.int32(each), '/', each, ' * ', activity_json["displayProperties"]['name'],
                      '/', d2_destiny_api_instance.milestone_types(activity_json['milestoneType']))
                activity_type = d2_destiny_api_instance.milestone_types(activity_json['milestoneType'])
                activity_name = activity_json["displayProperties"]['name']
                activity_type = d2_destiny_api_instance.milestone_types(activity_json['milestoneType'])
                activity_desc = activity_json["displayProperties"]['description']
                # activity_icon = activity_json["displayProperties"]['icon']
                activity_icon = None
                activity_has_variant = 0
                start_date = None
                end_date = None
                if int(each) == 2171429505 or int(each) == 3660836525 or int(each) == 3551755444:
                    # Find the Quests associated with a Milestone
                    for quest in api_response["Response"][each]["availableQuests"]:
                        quest_json = self.query_table('DestinyInventoryItemDefinition', quest["questItemHash"])
                        print(' >> ', quest_json['displayProperties']['name'], quest_json['displayProperties']['icon'])
                        quest_hash = quest["questItemHash"]
                        quest_name = quest_json['displayProperties']['name']
                        quest_desc = quest_json['displayProperties']['description']
                        quest_icon = quest_json['displayProperties']['icon']
                        q = Variants(parent_hash_id=int(each), modifier_type="Quest", hash_id=int(quest_hash),
                                     name=quest_name, description=quest_desc, icon=quest_icon)
                        q.save()
                        activity_has_variant = 1
                        try:
                            # Are there Modifiers for the Quest?
                            for modifier in quest["activity"]['modifierHashes']:
                                modifier_json = self.query_table('DestinyActivityModifierDefinition', modifier)
                                modifier_name = modifier_json['displayProperties']['name']
                                modifier_icon = modifier_json['displayProperties']['icon']
                                modifier_desc = modifier_json['displayProperties']['description']
                                print('   >> MODIFIERS ', modifier_name, modifier_icon, modifier_desc)
                                m = Variants(parent_hash_id=int(each), modifier_type="Modifier",
                                             hash_id=int(modifier),
                                             name=modifier_name, description=modifier_desc, icon=modifier_icon)
                                m.save()
                        except:
                            pass
                        for variant in quest["activity"]['variants']:
                            # Are there Variants to the Quest?
                            this_variant = variant['activityHash']
                            # print(this_variant)
                            variant_json = self.query_table('DestinyActivityDefinition', this_variant)
                            # print(variant_json)
                            variant_mode_hash = variant_json['directActivityModeHash']  # HEROIC nightfall: 1350109474
                            # print(variant_mode_hash)
                            variant_mode_json = self.query_table('DestinyActivityModeDefinition', variant_mode_hash)
                            variant_name = variant_mode_json['displayProperties']['name']
                            variant_icon = variant_mode_json['displayProperties']['icon']
                            variant_desc = variant_mode_json['displayProperties']['description']
                            print('   >> VARIANTS ', variant_name, variant_icon, variant_desc)
                            v = Variants(parent_hash_id=int(each), modifier_type="Variant", hash_id=int(this_variant),
                                         name=variant_name, description=variant_desc, icon=variant_icon)
                            v.save()
                            activity_has_variant = 1
                            for challenge in quest["challenges"]:
                                # print(challenge)
                                this_challenge = challenge["activityHash"]
                                if this_challenge == this_variant:
                                    challenge_json = self.query_table('DestinyObjectiveDefinition',
                                                                      challenge["objectiveHash"])
                                    # print(challenge_json)
                                    challenge_name = challenge_json['displayProperties']['name']
                                    # challenge_icon = challenge_json['displayProperties']['icon']
                                    challenge_desc = challenge_json['displayProperties']['description']
                                    print('     >> CHALLENGES ', challenge_name, challenge_desc, this_challenge)
                                    # print('     >> CHALLENGES ', challenge)
                                    c = Variants(parent_hash_id=int(this_variant), modifier_type="Challenge",
                                                 hash_id=int(challenge["objectiveHash"]),
                                                 name=challenge_name, description=challenge_desc, icon=variant_icon)
                                    c.save()
                                    # if int(each) == 3551755444:
                                    #     for vendor in api_response["Response"][each]["vendors"]:
                                    #         vendor_json = query_table('DestinyVendorDefinition', vendor['vendorHash'])
                                    #         print('    >> VENDOR ', vendor_json)
                    if int(each) == 3660836525 or int(each) == 3551755444:
                        now_date = datetime.now(timezone.utc)
                        start_date = dateparser.parse(api_response["Response"][each]["startDate"])
                        end_date = dateparser.parse(api_response["Response"][each]["endDate"])
                        print('  >> ', start_date, end_date, now_date)
                        print('  >> DATE DIFF', end_date - now_date)
                elif int(each) != 2171429505 and int(each) != 3245985898 and int(each) != 4109359897:
                    now_date = datetime.now(timezone.utc)
                    start_date = dateparser.parse(api_response["Response"][each]["startDate"])
                    end_date = dateparser.parse(api_response["Response"][each]["endDate"])
                    print('  >> ', start_date, end_date, now_date)
                    print('  >> DATE DIFF', end_date - now_date)
                m = Milestones(hash_id=int(each), event_type=activity_type, name=activity_name,
                               description=activity_desc,
                               icon=activity_icon, start_date=start_date, end_date=end_date,
                               has_variant=activity_has_variant)
                m.save()
            elif int(each) == 463010297:
                print(api.int32(each), '/', each, ' * ', activity_json['friendlyName'],
                      '/', d2_destiny_api_instance.milestone_types(activity_json['milestoneType']))
                # print(milestone_types(activity_json['milestoneType']))
                quest_hash = quest["questItemHash"]
                activity_type = d2_destiny_api_instance.milestone_types(activity_json['milestoneType'])
                activity_name = activity_json['friendlyName']
                activity_desc = quest_json['displayProperties']['description']
                activity_icon = quest_json['displayProperties']['icon']
                start_date = dateparser.parse(api_response["Response"][each]["startDate"])
                end_date = dateparser.parse(api_response["Response"][each]["endDate"])
                activity_has_variant = 1
                for quest in api_response["Response"][each]["availableQuests"]:
                    # print(quest.quest_item_hash)
                    quest_json = self.query_table('DestinyInventoryItemDefinition', quest["questItemHash"])
                    print('  > ', quest_json['displayProperties']['name'], quest_json['displayProperties']['icon'])
                    quest_hash = quest["questItemHash"]
                    quest_name = quest_json['displayProperties']['name']
                    quest_desc = quest_json['displayProperties']['description']
                    quest_icon = quest_json['displayProperties']['icon']
                    q = Variants(parent_hash_id=int(each), modifier_type="Quest", hash_id=int(quest_hash),
                                 name=quest_name, description=quest_desc, icon=quest_icon)
                    q.save()
                    activity_has_variant = 1
                m = Milestones(hash_id=int(each), event_type=activity_type, name=activity_name,
                               description=activity_desc,
                               icon=activity_icon, start_date=start_date, end_date=end_date,
                               has_variant=activity_has_variant)
                m.save()
            elif int(each) == 3245985898:
                print(api.int32(each), '/', each, ' * ', activity_json["displayProperties"]['name'],
                      '/', d2_destiny_api_instance.milestone_types(activity_json['milestoneType']))
                activity_name = activity_json["displayProperties"]['name']
                activity_type = d2_destiny_api_instance.milestone_types(activity_json['milestoneType'])
                activity_desc = activity_json["displayProperties"]['description']
                activity_icon = activity_json["displayProperties"]['icon']
                start_date = None
                end_date = None
                for quest in api_response["Response"][each]["availableQuests"]:
                    for variant in quest["activity"]['variants']:
                        this_variant = variant['activityHash']
                        variant_json = self.query_table('DestinyActivityDefinition', this_variant)
                        variant_name = variant_json['displayProperties']['name']
                        variant_icon = variant_json['displayProperties']['icon']
                        variant_desc = variant_json['displayProperties']['description']
                        print('   >> VARIANTS ', variant_name, variant_icon, variant_desc)
                        v = Variants(parent_hash_id=int(each), modifier_type="Variant", hash_id=int(this_variant),
                                     name=variant_name, description=variant_desc, icon=variant_icon)
                        v.save()
                        activity_has_variant = 1
                m = Milestones(hash_id=int(each), event_type=activity_type, name=activity_name,
                               description=activity_desc,
                               icon=activity_icon, start_date=start_date, end_date=end_date,
                               has_variant=activity_has_variant)
                m.save()
            elif int(each) == 534869653:
                # ITS XUR BABY
                print(api.int32(each), '/', each, ' * ', activity_json["displayProperties"]['name'],
                      '/', d2_destiny_api_instance.milestone_types(activity_json['milestoneType']))
                activity_name = activity_json["displayProperties"]['name']
                activity_type = d2_destiny_api_instance.milestone_types(activity_json['milestoneType'])
                activity_desc = activity_json["displayProperties"]['description']
                activity_icon = activity_json["displayProperties"]['icon']
                start_date = None
                end_date = None
                for vendor in api_response["Response"][each]["vendors"]:
                    vendor_hash = vendor['vendorHash']
                    vendor_json = self.query_table('DestinyVendorDefinition', vendor_hash)
                    vendor_name = vendor_json["displayProperties"]['name'] + ' ' + vendor_json["displayProperties"][
                        'subtitle']
                    vendor_desc = vendor_json["displayProperties"]['description']
                    vendor_icon = vendor_json["displayProperties"]['icon']
                    print('  > ', vendor_name, vendor_icon, vendor_desc)
                    v = Variants(parent_hash_id=int(each), modifier_type="Variant", hash_id=int(vendor_hash),
                                 name=vendor_name, description=vendor_desc, icon=vendor_icon)
                    v.save()
                    activity_has_variant = 1
                m = Milestones(hash_id=int(each), event_type=activity_type, name=activity_name,
                               description=activity_desc,
                               icon=activity_icon, start_date=start_date, end_date=end_date,
                               has_variant=activity_has_variant)
                m.save()
            else:
                print(api.int32(each), '/', each, ' * SUPPRESSED * ', activity_json['friendlyName'])
                # print(activity_json)
            # print(activity_name, activity_type)
            print('---')