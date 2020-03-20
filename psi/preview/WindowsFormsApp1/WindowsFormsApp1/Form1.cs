using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        System.Threading.AutoResetEvent quit_evt = new System.Threading.AutoResetEvent(false);
        Task t = null;
        public Form1()
        {
            InitializeComponent();
        }

        void load_image()
        {
            if (InvokeRequired)
            {
                this.Invoke(new Action(() => { load_image(); }));
            }
            else
            {
                try
                {
                    WebClient wc = new WebClient();
                    byte[] data = wc.DownloadData("http://192.168.5.39:5000/preview");
                    using (MemoryStream m = new MemoryStream(data))
                    {
                        pictureBox1.Image = Image.FromStream(m);
                    }
                }
                catch (Exception) { }
            }
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            //load_image();
            t= Task.Run(() =>
            {
                while (!quit_evt.WaitOne(5))
                {
                    load_image();
                    //System.Threading.Thread.Sleep(5);
                }
            });
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            quit_evt.Set();
            t.Wait(1000);
            Application.Exit();
        }
    }
}
