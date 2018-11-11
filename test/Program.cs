using Bonjour;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace test
{
    class Program
    {
        public static void logIt(String msg)
        {
            System.Diagnostics.Trace.WriteLine(msg);
        }
        [STAThread]
        static void Main(string[] args)
        {
            Task a = Task.Run(() => 
            {
                wait_for_exit(null);
            });
            System.Windows.Forms.Application.Run(new BonjourTest(null));
        }


        static void wait_for_exit(System.Collections.Specialized.StringDictionary args)
        {
            System.Console.WriteLine("press any key to terminate.");
            System.Console.ReadKey();
            //m_service.Browse(0, 0, "_airplay", null, m_eventManager);
            System.Windows.Forms.Application.Exit();
        }
    }
}
