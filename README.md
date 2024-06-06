_**Wazuh-IRIS-integration**_  
Simple Wazuh integration to send alerts to IRIS, as described in https://github.com/nateuribe/Wazuh-IRIS-integration

**Requirements**

*   Wazuh Server
*   IRIS
*   Python
*   python-requests
*   bash-script

  
**Installation**  
⚠️ IMPORTANT: By default, the IRIS Docker container utilizes self-signed certificates (https://docs.dfir-iris.org/operations/configuration/#certificates). If your setup is utilizing self-signed certificates, you will need to disable certificate verification with verify=False:

`response = requests.post(hook_url, verify=False, data=payload, headers={"Authorization": "Bearer " + api_key, "content-type": "application/json"})`


```plaintext

git clone https://github.com/edmondgodwin/iris-wazuh.git
cd iris-wazuh/
cp custom-iris.py /var/ossec/integrations/custom-iris.py
cp iris /var/ossec/integrations/iris
chmod 750 /var/ossec/integrations/custom-iris.py
chmod 750 /var/ossec/integrations/iris
chown root:wazuh /var/ossec/integrations/custom-iris.py
chown root:wazuh /var/ossec/integrations/iris
```

  
**Add the following snippet into the /var/ossec/etc/ossec.conf config file:**

```plaintext
<!-- ... Rest of config ... -->
<!-- IRIS integration -->
<integration>
 <name>custom-iris.py</name>
 <hook_url>http://IRIS-BASE-URL/alerts/add</hook_url>
 <level>7</level>
 <api_key>APIKEY</api_key>
 <alert_format>json</alert_format>
</integration>
<!-- ... Rest of config ... -->
```

  
Adjust `<hook_url>` and `<api_key>` to your environment, and change `<level>` to the desired threshold for alerts.

Restart the wazuh-manager service after making the above settings.

The IRIS API can be found in the Dashboard under My Settings.  
Since IRIS 2.4.7, you will need to add your IRIS user to the customer for which you are ingesting alerts for to see new entries in the alerts tab.

This can be configured by navigating to Advanced -> Access Control under Manage on the left panel, clicking on your user under Users, clicking on the Customers tab, and then Manage to add the customer (should be IrisInitialClient by default on a base install).

**Configuration**  
The script comes preconfigured with a basic payload to create new IRIS alerts. Use the Alerts API reference to modify this at will (https://docs.dfir-iris.org/latest/_static/iris_api_reference_v2.0.4.html#tag/Alerts/operation/post-case-add-alert).

Here are some notable values you may change in the custom-iris.py file:  
alert\_source\_link - URL from where the alert came from (Wazuh in this instance).

alert\_note - Note or comment to add to each alert.

alert\_customer\_id - Alerts in IRIS get assigned to "customers"; this is the ID of the customer for which the alerts pertain to.
