
# Enter mixins here


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        # print(kwargs)
        kwargs['request'] = self.request
        return kwargs