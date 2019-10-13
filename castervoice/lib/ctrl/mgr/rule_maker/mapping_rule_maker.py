from dragonfly import Grammar, AppContext
from castervoice.lib.ctrl.mgr.rule_maker.base_rule_maker import BaseRuleMaker
from castervoice.lib.merge.mergerule import MergeRule


class MappingRuleMaker(BaseRuleMaker):
    """
    Creates a MappingRule instance from the rule's class and a RuleDetails
    object, then runs all transformers over it.
    """

    def __init__(self, t_runner, smr_configurer):
        self._transformers_runner = t_runner
        self._smr_configurer = smr_configurer

    def create_non_ccr_grammar(self, managed_rule):
        details = managed_rule.get_details()
        rule_instance = managed_rule.get_rule_class()(name=details.name)

        if not details.transformer_exclusion:
            rule_instance = self._transformers_runner.transform_rule(rule_instance)

        self._smr_configurer.configure(rule_instance)
        if isinstance(rule_instance, MergeRule):
            rule_instance = rule_instance.to_mapping_rule()

        context = None
        if details.executable is not None or details.title is not None:
            context = AppContext(executable=details.executable, title=details.title)
        grammar = Grammar(details.grammar_name, context=context)
        grammar.add_rule(rule_instance)
        return grammar
