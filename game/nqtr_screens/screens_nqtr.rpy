init python:
    from pythonpackages.nqtr.navigation import is_closed_room
    from pythonpackages.nqtr.routine import commitment_background
    from pythonpackages.nqtr.action import current_button_actions, current_picture_in_background_actions

default afflvl = 0

screen room_navigation():

    modal True
    $ i = 0
    # More information by hovering the mouse
    $ (x,y) = renpy.get_mouse_pos()

    if dormitory_open:
        $ locations[2].hidden = False
    else:
        $ locations[2].hidden = True

    if inventory_open:
        use inventory_screen(first_inventory=mc_inventory)

    elif (map_open and cur_map_id):
        use map(maps, cur_map_id)

        if (not info_open):
            for location in locations:
                # If the Map where I am is the same as the Map where the room is located
                use location_button(location)

    elif (not info_open):
        # Rooms
        hbox:
            yalign 0.99
            xalign 0.01
            spacing 2

            for room in rooms:
                $ i += 1

                # Check the presence of ch in that room
                $ there_are_ch = False
                for comm in commitments_in_cur_location.values():
                    # If it is the selected room
                    if comm != None and room.id == comm.room_id:
                        # I insert hbox only if they are sure that someone is there
                        $ there_are_ch = True

                use room_button(room, cur_room, i, there_are_ch)

        # Action wich Picture in background
        for room in rooms:
            # Adds the button list of possible actions in that room
            if (cur_room and room.id == cur_room.id and not room.id in closed_rooms):
                for act in current_picture_in_background_actions(actions= actions | df_actions, room = room, now_hour = tm.hour , current_day = tm.day, tm = tm, flags = flags):
                    use action_picture_in_background(act)

        # Normal Actions (with side button)
        vbox:
            yalign 0.95
            xalign 0.99
            for room in rooms:
                # Adds the button list of possible actions in that room
                if (cur_room and room.id == cur_room.id):
                    for act in current_button_actions(actions= actions | df_actions, room = room, now_hour = tm.hour , current_day = tm.day, tm = tm, flags = flags):
                        use action_button(act)

                # Talk
                # Adds a talk for each ch (NPC) and at the talk interval adds the icon for each secondary ch
                for comm in commitments_in_cur_location.values():
                    if (cur_room and comm and room.id == comm.room_id and room.id == cur_room.id):
                        # Insert in talk for every ch, main in that room
                        for conversation in comm.conversations:
                            if (conversation):
                                use action_talk_button(conversation, comm.conversation_background(conversation.character))

            # Fixed button to wait
            use wait_button()

    # Time
    use time_text(tm, show_wait_button = map_open)

    hbox:
        align (0.01, 0.01)
        spacing 2

        imagebutton:
            idle '/gui/interface/settings.webp'
            focus_mask True
            action ShowMenu('save')
            if renpy.variant("pc"):
                tooltip _("Settings")
            at dr_button_menu_transform

        imagebutton:
            idle '/gui/interface/help.webp'
            focus_mask True
            action ShowMenu('help')
            if renpy.variant("pc"):
                tooltip _("Help")
            at dr_button_menu_transform

        if len(current_quest_stages) > 0 :
            imagebutton:
                idle '/gui/interface/quest.webp'
                focus_mask True
                action [
                    SetVariable('cur_task_menu', ""),
                    SetVariable('cur_quest_menu', ""),
                    SetVariable('quest_open', True),
                    Show('menu_memo'),
                ]
                if renpy.variant("pc"):
                    tooltip _("Quests")
                at dr_button_menu_transform

        if info_open == False:
            imagebutton:
                idle '/gui/interface/info.webp'
                focus_mask True
                action [Show("affection_main"), SetVariable('info_open', True)]
                if renpy.variant("pc"):
                    tooltip _("Characters info")
                at dr_button_menu_transform
        else:
            imagebutton:
                idle '/gui/interface/info.webp'
                focus_mask True
                action [Hide("affection_main"), Hide("affection_ayumi"), Hide("affection_akane"), SetVariable('info_open', False)]
                if renpy.variant("pc"):
                    tooltip _("Characters info")
                at dr_button_menu_transform

    hbox:
        align (0.99, 0.01)
        spacing 2

        # Money
        text "$[mc_inventory.money]":
            align(1.0, 0.5)
            size gui.interface_text_size
            drop_shadow [(2, 2)]

        if renpy.has_label("open_inventory"):
            imagebutton:
                idle '/gui/interface/inventory.webp'
                focus_mask True
                action [Call("after_return_from_room_navigation1", label_name_to_call = "open_inventory")]
                if renpy.variant("pc"):
                    tooltip _("Backpack")
                at dr_button_menu_transform

        if renpy.has_label("open_phone"):
            imagebutton:
                idle '/gui/interface/phone.webp'
                focus_mask True
                action Call("after_return_from_room_navigation1", label_name_to_call = "open_phone")
                if renpy.variant("pc"):
                    tooltip _("Phone")
                at dr_button_menu_transform

        if renpy.has_label("open_map"):
            imagebutton:
                idle '/gui/interface/map.webp'
                focus_mask True
                action [Call("after_return_from_room_navigation1", label_name_to_call = "open_map")]
                tooltip _("Map")
                at dr_button_menu_transform

    # More information by hovering the mouse
    if renpy.variant("pc"):
        $ text = GetTooltip()
        if text:
            text "[text]":
                xpos x-20
                ypos y-20
                size gui.dr_little_text_size 
                drop_shadow [(2, 2)] 
                outlines [(2, "#000", 0, 1)]

label set_background_nqtr:
    if (not map_open):
        if(is_closed_room(room_id= cur_room.id, closed_rooms= closed_rooms, now_hour= tm.hour, tm = tm)):
            call closed_room_event from _call_closed_room_event
        else:
            $ sp_bg_change_room = commitment_background(commitments_in_cur_location, cur_room.id)
            call set_room_background(sp_bg_change_room) from _call_set_room_background
    return

label set_room_background(sp_bg_change_room = ""):
    if (not isNullOrEmpty(sp_bg_change_room)):
        call set_background(sp_bg_change_room) from _call_set_background
    else:
        call set_background(cur_room.background) from _call_set_background_1
    return

# making calls safely:
# Why? Because if I use Call("label") in sleep mode from the room_navigation
# and in the "label" I use "return" an almost all cases the game will end.
label after_return_from_room_navigation(label_name_to_call = ""):
    if isNullOrEmpty(label_name_to_call):
        $ log_error("label_name_to_call is empty", renpy.get_filename_line())
    elif not renpy.has_label(label_name_to_call):
        $ log_error("label_name_to_call: " + label_name_to_call + " not found", renpy.get_filename_line())
    else:
        $ renpy.call(label_name_to_call)
    call set_background_nqtr from _call_set_background_nqtr
    call screen room_navigation with Dissolve(0.25)
    $ log_error("thera is a anomaly in room_navigation. value: " + label_name_to_call, renpy.get_filename_line())
    jump after_return_from_room_navigation

label after_return_from_room_navigation1(label_name_to_call = ""):
    if isNullOrEmpty(label_name_to_call):
        $ log_error("label_name_to_call is empty", renpy.get_filename_line())
    elif not renpy.has_label(label_name_to_call):
        $ log_error("label_name_to_call: " + label_name_to_call + " not found", renpy.get_filename_line())
    else:
        $ renpy.call(label_name_to_call)
    call set_background_nqtr from _call_set_background_nqtr_2
    call screen room_navigation
    $ log_error("thera is a anomaly in room_navigation. value: " + label_name_to_call, renpy.get_filename_line())
    jump after_return_from_room_navigation
