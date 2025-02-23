from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        context['example'] = 'example injected by context hook'
