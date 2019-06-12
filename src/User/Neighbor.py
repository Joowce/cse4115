from User.User import UserType


class Neighbor(object):
    def __init__(self,
                 name=None, public_key=None, conn=None,
                 addr=None, user_type=None, total_dict=None):
        if total_dict is None:
            total_dict = dict()
        self.name = name or total_dict.get('name')
        self.public_key = public_key or total_dict.get('public_key')
        self.addr = addr or total_dict.get('addr')
        self.conn = conn or total_dict.get('conn')
        self.type = user_type or UserType[total_dict.get('type')]

    def get_summary(self):
        summary = vars(self).copy()
        summary['type'] = self.type.name
        del(summary['conn'])
        return summary
