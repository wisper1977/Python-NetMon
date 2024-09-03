from pysnmp.hlapi.asyncio import getCmd, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, SnmpEngine
import asyncio

class NetOpsSNMP:
    def __init__(self, community_string="public", logger=None):
        self.community_string = community_string
        self.logger = logger

    async def snmp_get(self, ip_address, oid):
        try:
            # Create the SNMP GET command
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community_string, mpModel=0),  # mpModel=0 is for SNMPv1/v2c
                UdpTransportTarget((ip_address, 161), timeout=2, retries=3),  # Adjust timeout and retries as needed
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )

            # Fetch the result
            errorIndication, errorStatus, errorIndex, varBinds = await iterator

            # Handle potential errors
            if errorIndication:
                if self.logger:
                    self.logger.log("ERROR", f"SNMP error for {ip_address}: {errorIndication}")
                return None
            elif errorStatus:
                if self.logger:
                    self.logger.log("ERROR", f"SNMP error for {ip_address}: {errorStatus.prettyPrint()}")
                return None
            else:
                # Extract the result from varBinds
                result = varBinds[0].prettyPrint().split('= ')[1]
                if self.logger:
                    self.logger.log("INFO", f"SNMP response for {ip_address}: {result}")
                return result

        except Exception as e:
            if self.logger:
                self.logger.log("ERROR", f"SNMP error for {ip_address}: {str(e)}")
            return None