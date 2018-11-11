using Bonjour;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace test
{
    class BonjourTest : ApplicationContext
    {
        DNSSDService m_service = null;
        DNSSDEventManager m_eventManager = null;

        public BonjourTest(System.Collections.Specialized.StringDictionary args)
        {
            m_service = new Bonjour.DNSSDService();
            m_eventManager = new DNSSDEventManager();
            m_eventManager.ServiceFound += M_eventManager_ServiceFound;
            m_eventManager.ServiceResolved += M_eventManager_ServiceResolved;
            m_eventManager.QueryRecordAnswered += M_eventManager_QueryRecordAnswered;

            //m_service.Browse(0, 0, "_p2pchat._udp", null, m_eventManager);
            //m_service.Browse(0, 0, "_services._dns-sd._udp", null, m_eventManager);
            //m_service.Browse(0, 0, "_airplay._tcp", null, m_eventManager);
            m_service.Browse(0, 0, "_http._tcp", null, m_eventManager);

            //Task a = Task.Run(()=> { run(); });
            this.ThreadExit += BonjourTest_ThreadExit;
        }

        private void BonjourTest_ThreadExit(object sender, EventArgs e)
        {
            //throw new NotImplementedException();
        }

        private void M_eventManager_QueryRecordAnswered(DNSSDService service, DNSSDFlags flags, uint ifIndex, string fullname, DNSSDRRType rrtype, DNSSDRRClass rrclass, object rdata, uint ttl)
        {
            if (rdata is byte[])
            {
                IPAddress addr = new IPAddress(rdata as byte[]);
            }
        }

        private void M_eventManager_ServiceResolved(DNSSDService service, DNSSDFlags flags, uint ifIndex, string fullname, string hostname, ushort port, TXTRecord record)
        {
            Program.logIt($"fullname={fullname}, hostname={hostname}, port={port}");
            if (record != null)
            {
                uint count = record.GetCount();
                for (uint i = 0; i < count; i++)
                {
                    string k = record.GetKeyAtIndex(i);
                    dynamic v = record.GetValueAtIndex(i);
                }
            }
            m_service.QueryRecord(0, ifIndex, hostname, DNSSDRRType.kDNSSDType_A, DNSSDRRClass.kDNSSDClass_IN, m_eventManager);
        }

        private void M_eventManager_ServiceFound(DNSSDService browser, DNSSDFlags flags, uint ifIndex, string serviceName, string regtype, string domain)
        {
            Program.logIt($"serviceName={serviceName}");
            if (string.Compare("mywebservice", serviceName) == 0)
            {
                m_service.Resolve(0, ifIndex, serviceName, regtype, domain, m_eventManager);
            }
        }

        void run()
        {

        }
    }
}
