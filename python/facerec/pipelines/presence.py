

class PresencePipeline:
    def __init__(self, pipeline_register):
        self.p_reg = pipeline_register

        # store presence data ordered by time;
        # first set in list is the most recent.
        self.presence = {
            'entering': set(),
            'current': set(),
            'leaving': set(),
            'recent': set(),
            'ago': set(),
        }

    def _update_presence(self, frame):
        self.presence['ago'] = self.presence['recent']
        self.presence['recent'] = self.presence['current']
        self.presence['current'] = set([(profile_id, name)
                                        for profile_id, name, _, _ in
                                        self.p_reg.face_profiles])

        self.presence['entering'] = self.presence['current'] - \
            self.presence['recent']
        self.presence['leaving'] = self.presence['recent'] - \
            self.presence['current']

        for profile_id, name in self.presence['leaving']:
            self.p_reg.hooks.on_face_disappear(profile_id, name)

        if len(self.presence['ago']) > 0 and len(self.presence['current']) == 0:
            self.p_reg.hooks.on_all_leave(frame)

        # print('entering:', [name for _, name in self.presence['entering']])
        # print('current:', [name for _, name in self.presence['current']])
        # print('leaving:', [name for _, name in self.presence['leaving']])

    def _trigger_presence_hooks(self, frame, location, profile):
        # adjust the location to account rgb small frame
        top, right, bottom, left = location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        profile_id, name, file, face_encoding = profile
        presence = (profile_id, name)

        face_crop = frame[top - 10:bottom + 10, left - 10: right + 10]
        if presence in self.presence['entering']:
            if profile_id is None:
                self.p_reg.hooks.on_face_unknown(face_crop, face_encoding)
            else:
                self.p_reg.hooks.on_face_appear(
                    face_crop, profile_id, name, file)

    def process(self, frame, w, h, args: tuple):
        update_presence, location, profile = args
        if update_presence:
            self._update_presence(frame)
        self._trigger_presence_hooks(frame, location, profile)
