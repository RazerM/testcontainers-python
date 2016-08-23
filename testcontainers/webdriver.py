#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from testcontainers import config
from testcontainers.generic import DockerContainer
from testcontainers.waiting_utils import wait_container_is_ready


class WebDriverDockerContainer(DockerContainer):
    def __init__(self, capabilities=DesiredCapabilities.FIREFOX):
        super(WebDriverDockerContainer, self).__init__()
        self._capabilities = capabilities
        self._default_port = 4444

    def start(self):
        """
        Start selenium containers and wait until they are ready
        :return:
        """
        self._docker.run(**config.hub)
        if self._capabilities["browserName"] == "firefox":
            self._docker.run(**config.firefox_node)
        else:
            self._docker.run(**config.chrome_node)
        return self

    @wait_container_is_ready()
    def driver(self):
        return webdriver.Remote(
            command_executor=('http://{}:{}/wd/hub'.format(
                config.selenium_hub_host, self._default_port)),
            desired_capabilities=self._capabilities)