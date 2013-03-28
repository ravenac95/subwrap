import fudge
from fudge.inspector import arg
from nose.tools import *
import subwrap


def test_simple_run():
    output1 = subwrap.run(['echo', 'hello'])
    assert output1.std_out.strip() == 'hello'


@fudge.patch('subprocess.Popen')
def test_simple_run_with_fake(fake_popen):
    fake_process = fake_popen.expects_call().returns_fake()
    fake_process.expects('communicate').returns(('hello', ''))
    fake_process.has_attr(returncode=0)

    output = subwrap.run(['somecmd'])
    assert output.std_out == 'hello'


@raises(subwrap.CommandError)
@fudge.patch('subprocess.Popen')
def test_default_exit_handle_with_fake(fake_popen):
    fake_process = fake_popen.expects_call().returns_fake()
    fake_process.expects('communicate').returns(('', ''))
    fake_process.has_attr(returncode=1)

    subwrap.run(['somecmd'])


@fudge.patch('subprocess.Popen')
def test_custom_exit_handle_with_fake(fake_popen):
    fake_process = fake_popen.expects_call().returns_fake()
    fake_process.expects('communicate').returns(('', ''))
    fake_process.has_attr(returncode=1000)

    def custom_handle(response):
        assert response.return_code == 1000

    subwrap.run(['somecmd'], exit_handle=custom_handle)


@fudge.patch('subprocess.Popen')
def test_pass_options(fake_popen):
    any = arg.any
    fake_process = (fake_popen.expects_call()
            .with_args(any(), cwd="test", stderr=any(), stdout=any())
            .returns_fake())
    fake_process.expects('communicate').returns(('', ''))
    fake_process.has_attr(returncode=0)
    subwrap.run(['somecmd'], cwd="test")
