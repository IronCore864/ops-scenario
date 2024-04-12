import ops
import pytest

import scenario


class MyCharm(ops.CharmBase):
    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        for evt in self.on.events().values():
            self.framework.observe(evt, self._on_event)

    def _on_event(self, event):
        pass


def test_get_cloud_spec():
    cloud_spec = ops.CloudSpec.from_dict({
        'type': 'lxd',
        'name': 'localhost',
        'endpoint': 'https://10.76.251.1:8443',
        'credential': {
            'auth-type': 'certificate',
            'attrs': {
                'client-cert': 'foo',
                'client-key': 'bar',
                'server-cert': 'baz'
            }
        }
    })
    ctx = scenario.Context(MyCharm, meta={"name": "foo"})
    state = scenario.State(
        cloud_spec=cloud_spec,
        model=scenario.Model(name="lxd-model", type="lxd"),
    )
    with ctx.manager("start", state=state) as mgr:
        assert mgr.charm.model.get_cloud_spec() == cloud_spec


def test_get_cloud_spec_error():
    ctx = scenario.Context(MyCharm, meta={"name": "foo"})
    state = scenario.State(model=scenario.Model(name="lxd-model", type="lxd"))
    with ctx.manager("start", state) as mgr:
        with pytest.raises(ops.ModelError):
            mgr.charm.model.get_cloud_spec()
