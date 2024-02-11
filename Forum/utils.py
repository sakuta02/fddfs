class DataMixin:
    flag = None
    paginate_by = 7

    def get_mixin_context(self, context, **kwargs):
        if self.flag == 1:
            context.update(kwargs)
            return context
        elif self.flag == 2:
            context.update(kwargs)
            return context
