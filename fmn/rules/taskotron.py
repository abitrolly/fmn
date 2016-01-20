from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('taskotron.result.new')])
def taskotron_result_new(config, message):
    """ New taskotron task result

    This rule lets through messages from the `taskotron
    <https://taskotron.fedoraproject.org>`_ about new task result.
    """
    return message['topic'].endswith('taskotron.result.new')


@hint(categories=['taskotron'])
def taskotron_task(config, message, task=None):
    """ Particular taskotron task

    With this rule, you can limit messages to only those of particular
    `taskotron <https://taskotron.fedoraproject.org/>`_ task.

    You can specify several tasks by separating them with a comma ',',
    i.e.: ``depcheck,rpmlint``.
    """

    if not task:
        return False

    tasks = [item.strip().lower() for item in task.split(',')]
    return message['msg']['task'].get('name').lower() in tasks


@hint(categories=['taskotron'])
def taskotron_changed_outcome(config, message):
    """ Taskotron task outcome changed

    With this rule, you can limit messages to only those task results
    with changed outcomes. This is useful when an object (a build,
    an update, etc) gets retested and either the object itself or the
    environment changes and the task outcome is now different (e.g.
    FAILED -> PASSED).
    """

    outcome = message['msg']['result'].get('outcome')
    prev_outcome = message['msg']['result'].get('prev_outcome')

    return outcome != prev_outcome


@hint(categories=['taskotron'])
def taskotron_task_outcome(config, message, outcome=None):
    """ Particular taskotron task outcome

    With this rule, you can limit messages to only those of particular
    `taskotron <https://taskotron.fedoraproject.org/>`_ task outcome.

    You can specify several outcomes by separating them with a comma ',',
    i.e.: ``PASSED,FAILED``.

    The full list of supported outcomes can be found in the libtaskotron
    `documentation <https://docs.qadevel.cloud.fedoraproject.org/
    libtaskotron/latest/resultyaml.html#minimal-version>`_.
    """

    if not outcome:
        return False

    outcomes = [item.strip().lower() for item in outcome.split(',')]
    return message['msg']['result'].get('outcome').lower() in outcomes


@hint(categories=['taskotron'])
def taskotron_task_failed_or_changed_outcome(config, message):
    """ Taskotron task failed or changed outcome

    With this rule, you can limit messages to only those task results
    with FAILED outcome or those with changed outcomes. This rule is
    a handy way of filtering a very useful use case - being notified
    when either check failed for an item (a build, an update, etc),
    or the item was fixed and the check now passes (i.e. changed
    outcome).
    """

    outcome = message['msg']['result'].get('outcome')
    prev_outcome = message['msg']['result'].get('prev_outcome')

    return outcome == 'FAILED' or outcome != prev_outcome


@hint(categories=['taskotron'])
def taskotron_release_critical_task(config, message):
    """ Release-critical taskotron tasks

    With this rule, you can limit messages to only those of
    release-critical
    `taskotron <https://taskotron.fedoraproject.org/>`_ task.

    These are the checks which are deemed extremely important
    by the distribution, and their failure should be carefully
    inspected. Currently these checks are ``depcheck`` and
    ``upgradepath``.
    """

    task = message['msg']['task'].get('name')

    return task in ['depcheck', 'upgradepath']
