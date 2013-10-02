from cube2common.stream_specification import Field, FieldCollection, IteratedFieldCollection, TerminatedFieldCollection
from cube2common.stream_specification import MessageType, StreamStateModifierType, StreamSpecification
from cube2common.stream_specification import RawField, SwitchField, CaseField
from cube2common.read_cube_data_stream import ReadCubeDataStream as CubeDataStream
from cube2common.constants import message_types, cs_id_types

type_method_mapping = {
                            'stream_data': CubeDataStream.read,
                            'int': CubeDataStream.getint, 
                            'uint': CubeDataStream.getuint,
                            'string': CubeDataStream.getstring, 
                            'float': CubeDataStream.getfloat
                      }

sauerbraten_stream_spec = StreamSpecification(CubeDataStream, type_method_mapping, {}, "int", message_types)

mt = MessageType("N_CONNECT", 
        Field(name="name", type="string"),
        Field(name="playermodel", type="int"),
        Field(name="pwdhash", type="string"),
        Field(name="authdomain", type="string"),
        Field(name="authname", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_CONNECT, mt)

mt = MessageType("N_CHECKMAPS")
sauerbraten_stream_spec.add_message_type(message_types.N_CHECKMAPS, mt)

mt = MessageType("N_EDITMODE",
        Field(name="value", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_EDITMODE, mt)

mt = MessageType("N_PING",
        Field(name="cmillis", type="int"))
sauerbraten_stream_spec.add_message_type(   message_types.N_PING, mt)

mt = MessageType("N_TRYSPAWN")
sauerbraten_stream_spec.add_message_type(message_types.N_TRYSPAWN, mt)

sm = StreamStateModifierType(Field(name="aiclientnum", type="int"))
sauerbraten_stream_spec.add_state_modifier_type(message_types.N_FROMAI, sm)
                            
mt = MessageType("N_SHOOT",
        Field(name="shot_id", type="int"),
        Field(name="gun", type="int"),
        Field(name="fx", type="int"),
        Field(name="fy", type="int"),
        Field(name="fz", type="int"),
        Field(name="tx", type="int"),
        Field(name="ty", type="int"),
        Field(name="tz", type="int"),
        
        IteratedFieldCollection(
                name="hits",
                count=Field(type="int"),
                field_collection=FieldCollection(
                                Field(name="target_cn", type="int"),
                                Field(name="lifesequence", type="int"),
                                Field(name="distance", type="int"),
                                Field(name="rays", type="int"),
                                Field(name="dx", type="int"),
                                Field(name="dy", type="int"),
                                Field(name="dz", type="int")
                )))
sauerbraten_stream_spec.add_message_type(message_types.N_SHOOT, mt)

mt = MessageType("N_EXPLODE",
        Field(name="cmillis", type="int"),
        Field(name="gun", type="int"),
        Field(name="explode_id", type="int"),
        
        IteratedFieldCollection(
                name="hits",
                count=Field(type="int"),
                field_collection=FieldCollection(
                                Field(name="target_cn", type="int"),
                                Field(name="lifesequence", type="int"),
                                Field(name="distance", type="int"),
                                Field(name="rays", type="int"),
                                Field(name="dx", type="int"),
                                Field(name="dy", type="int"),
                                Field(name="dz", type="int")
                )))
sauerbraten_stream_spec.add_message_type(message_types.N_EXPLODE, mt)

mt = MessageType("N_GUNSELECT",
        Field(name="gunselect", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_GUNSELECT, mt)

mt = MessageType("N_SPAWN",
        Field(name="lifesequence", type="int"),
        Field(name="gunselect", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_SPAWN, mt)

mt = MessageType("N_SUICIDE")
sauerbraten_stream_spec.add_message_type(message_types.N_SUICIDE, mt)

mt = MessageType("N_CLIENTPING",
        Field(name="ping", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_CLIENTPING, mt)

mt = MessageType("N_TAUNT")
sauerbraten_stream_spec.add_message_type(message_types.N_TAUNT, mt)

mt = MessageType("N_MAPCRC",
        Field(name="map_name", type="string"),
        Field(name="mapcrc", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_MAPCRC, mt)

mt = MessageType("N_INITFLAGS",
                IteratedFieldCollection(
                name="flags",
                count=Field(type="int"),
                field_collection=FieldCollection(Field(name="team", type="int"),
                                                 Field(name="x", type="int"),
                                                 Field(name="y", type="int"),
                                                 Field(name="z", type="int"))))
sauerbraten_stream_spec.add_message_type(message_types.N_INITFLAGS, mt)

mt = MessageType("N_TRYDROPFLAG")
sauerbraten_stream_spec.add_message_type(message_types.N_TRYDROPFLAG, mt)

mt = MessageType("N_TAKEFLAG",
        Field(name="flag", type="int"),
        Field(name="version", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_TAKEFLAG, mt)

mt = MessageType("N_BASES",
                IteratedFieldCollection(
                name="bases",
                count=Field(type="int"),
                field_collection=FieldCollection(Field(name="ammotype", type="int"),
                                                 Field(name="x", type="int"),
                                                 Field(name="y", type="int"),
                                                 Field(name="z", type="int"))))
sauerbraten_stream_spec.add_message_type(message_types.N_BASES, mt)

mt = MessageType("N_REPAMMO")
sauerbraten_stream_spec.add_message_type(message_types.N_REPAMMO, mt)

mt = MessageType("N_ITEMLIST",
        TerminatedFieldCollection(name="items",
                                    terminator_field=Field(type="int"),
                                    terminator_comparison=lambda t: t >= 0,
                                    field_collection=FieldCollection(
                                                                 Field(name="item_index", type="int"),
                                                                 Field(name="item_type", type="int")))
                 )
sauerbraten_stream_spec.add_message_type(message_types.N_ITEMLIST, mt)

mt = MessageType("N_SOUND",
        Field(name="sound", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_SOUND, mt)

mt = MessageType("N_ITEMPICKUP",
        Field(name="item_index", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_ITEMPICKUP, mt)

mt = MessageType("N_TEXT",
        Field(name="text", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_TEXT, mt)

mt = MessageType("N_SAYTEAM",
        Field(name="text", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_SAYTEAM, mt)

mt = MessageType("N_SWITCHNAME",
        Field(name="name", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_SWITCHNAME, mt)

mt = MessageType("N_SWITCHMODEL",
        Field(name="playermodel", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_SWITCHMODEL, mt)

mt = MessageType("N_SWITCHTEAM",
        Field(name="team", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_SWITCHTEAM, mt)

mt = MessageType("N_MAPCHANGE",
        Field(name="map_name", type="string"),
        Field(name="mode_num", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_MAPCHANGE, mt)

mt = MessageType("N_MAPVOTE",
        Field(name="map_name", type="string"),
        Field(name="mode_num", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_MAPVOTE, mt)

mt = MessageType("N_MASTERMODE",
        Field(name="mastermode", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_MASTERMODE, mt)

mt = MessageType("N_KICK",
        Field(name="target_cn", type="int"),
        Field(name="reason", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_KICK, mt)

mt = MessageType("N_CLEARBANS")
sauerbraten_stream_spec.add_message_type(message_types.N_CLEARBANS, mt)

mt = MessageType("N_SPECTATOR",
        Field(name="target_cn", type="int"),
        Field(name="value", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_SPECTATOR, mt)

mt = MessageType("N_SETTEAM",
        Field(name="target_cn", type="int"),
        Field(name="team", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_SETTEAM, mt)

mt = MessageType("N_RECORDDEMO",
        Field(name="value", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_RECORDDEMO, mt)

mt = MessageType("N_CLEARDEMOS",
        Field(name="demonum", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_CLEARDEMOS, mt)

mt = MessageType("N_LISTDEMOS")
sauerbraten_stream_spec.add_message_type(message_types.N_LISTDEMOS, mt)

mt = MessageType("N_STOPDEMO")
sauerbraten_stream_spec.add_message_type(message_types.N_STOPDEMO, mt)

mt = MessageType("N_GETDEMO",
        Field(name="demonum", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_GETDEMO, mt)

mt = MessageType("N_GETMAP")
sauerbraten_stream_spec.add_message_type(message_types.N_GETMAP, mt)

mt = MessageType("N_FORCEINTERMISSION",
        Field(name="size", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_FORCEINTERMISSION, mt)

mt = MessageType("N_NEWMAP",
        Field(name="size", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_NEWMAP, mt)

mt = MessageType("N_SETMASTER",
        Field(name="target_cn", type="int"),
        Field(name="value", type="int"),
        Field(name="pwdhash", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_SETMASTER, mt)

mt = MessageType("N_AUTHTRY",
        Field(name="authdomain", type="string"),
        Field(name="authname", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_AUTHTRY, mt)

mt = MessageType("N_AUTHKICK",
        Field(name="authdomain", type="string"),
        Field(name="authname", type="string"),
        Field(name="target_cn", type="int"),
        Field(name="reason", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_AUTHKICK, mt)

mt = MessageType("N_AUTHANS",
        Field(name="authdomain", type="string"),
        Field(name="authid", type="int"),
        Field(name="answer", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_AUTHANS, mt)

mt = MessageType("N_ADDBOT",
        Field(name="skill", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_ADDBOT, mt)

mt = MessageType("N_DELBOT")
sauerbraten_stream_spec.add_message_type(message_types.N_DELBOT, mt)

mt = MessageType("N_BOTLIMIT",
        Field(name="limit", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_BOTLIMIT, mt)

mt = MessageType("N_BOTBALANCE",
        Field(name="balance", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_BOTBALANCE, mt)

mt = MessageType("N_GAMESPEED",
        Field(name="value", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_GAMESPEED, mt)

mt = MessageType("N_PAUSEGAME",
        Field(name="value", type="int"))
sauerbraten_stream_spec.add_message_type(message_types.N_PAUSEGAME, mt)

mt = MessageType("N_SERVCMD",
        Field(name="command", type="string"))
sauerbraten_stream_spec.add_message_type(message_types.N_SERVCMD, mt)

mt = MessageType("N_CLIPBOARD",
        Field(name="clientnum", type="int"),
        Field(name="unpacklen", type="int"),
        IteratedFieldCollection(
            name="data",
            count=Field(type="int"),
            field_collection=RawField(size=1)))
sauerbraten_stream_spec.add_message_type(message_types.N_CLIPBOARD, mt)

common_edit_fields = [Field(name="sel_ox", type="int"),
                      Field(name="sel_oy", type="int"),
                      Field(name="sel_oz", type="int"),
                      
                      Field(name="sel_sx", type="int"),
                      Field(name="sel_sy", type="int"),
                      Field(name="sel_sz", type="int"),
                      
                      Field(name="sel_grid", type="int"),
                      Field(name="sel_orient", type="int"),
                      
                      Field(name="sel_cx", type="int"),
                      Field(name="sel_cxs", type="int"),
                      Field(name="sel_cy", type="int"),
                      Field(name="sel_cys", type="int"),
                      
                      Field(name="sel_corner", type="int")]

mtf = common_edit_fields + [Field(name="direction", type="int"),
                            Field(name="mode", type="int")]
mt = MessageType("N_EDITF", *mtf)
sauerbraten_stream_spec.add_message_type(message_types.N_EDITF, mt)

mtf = common_edit_fields + [Field(name="texture", type="int"),
                            Field(name="all_faces", type="int")]
mt = MessageType("N_EDITT", *mtf)
sauerbraten_stream_spec.add_message_type(message_types.N_EDITT, mt)

mtf = common_edit_fields + [Field(name="material", type="int"),
                            Field(name="material_filter", type="int")]
mt = MessageType("N_EDITM", *mtf)
sauerbraten_stream_spec.add_message_type(message_types.N_EDITM, mt)

mt = MessageType("N_FLIP", *common_edit_fields)
sauerbraten_stream_spec.add_message_type(message_types.N_FLIP, mt)

mt = MessageType("N_COPY", *common_edit_fields)
sauerbraten_stream_spec.add_message_type(message_types.N_COPY, mt)

mt = MessageType("N_PASTE", *common_edit_fields)
sauerbraten_stream_spec.add_message_type(message_types.N_PASTE, mt)

mt = MessageType("N_ROTATE",
        *(common_edit_fields +
        [Field(name="axis", type="int")]))
sauerbraten_stream_spec.add_message_type(message_types.N_ROTATE, mt)

mt = MessageType("N_REPLACE",
        *(common_edit_fields +
          [Field(name="texture", type="int"),
           Field(name="new_texture", type="int"),
           Field(name="in_selection", type="int")]))
sauerbraten_stream_spec.add_message_type(message_types.N_REPLACE, mt)

mt = MessageType("N_DELCUBE", *common_edit_fields)
sauerbraten_stream_spec.add_message_type(message_types.N_DELCUBE, mt)

mt = MessageType("N_REMIP")
sauerbraten_stream_spec.add_message_type(message_types.N_REMIP, mt)

mt = MessageType("N_EDITENT",
        Field(name="entid", type="int"),
        Field(name="x", type="int"),
        Field(name="y", type="int"),
        Field(name="z", type="int"),
        Field(name="type", type="int"),
        IteratedFieldCollection(
            name="attrs",
            count=5,
            field_collection=Field(type="int")))
sauerbraten_stream_spec.add_message_type(message_types.N_EDITENT, mt)

mt = MessageType("N_EDITVAR",
        Field(name="clientnum", type="int"), 
        SwitchField(
            predicate=Field(type="int"), 
            cases=[
                CaseField(predicate_comparison = lambda t: t == cs_id_types.ID_VAR,
                          consequent=FieldCollection(
                                         Field(name="var_type", type="int"),
                                         Field(name="var_name", type="string"),
                                         Field(name="var_value", type="int"))),
                CaseField(predicate_comparison = lambda t: t == cs_id_types.ID_FVAR,
                          consequent=FieldCollection(
                                         Field(name="var_type", type="int"),
                                         Field(name="var_name", type="string"),
                                         Field(name="var_value", type="float"))),
                CaseField(predicate_comparison = lambda t: t == cs_id_types.ID_SVAR,
                          consequent=FieldCollection(
                                         Field(name="var_type", type="int"),
                                         Field(name="var_name", type="string"),
                                         Field(name="var_value", type="string")))
            ],
            default=FieldCollection(Field(name="var_type", type="int"),
                                    Field(name="var_name", type="string")),
            peek_predicate=True))
sauerbraten_stream_spec.add_message_type(message_types.N_EDITVAR, mt)
