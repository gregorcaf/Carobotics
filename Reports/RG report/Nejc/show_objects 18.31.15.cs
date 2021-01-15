using System.Collections;
using System.Collections.Generic;
using System.Net;//to 
using System.IO;//to
using System; 
using UnityEngine;

[System.Serializable]
public class CarStateJson
{
    public string brake;
    public bool gear_immediate;
    public bool handbrake;
    public bool is_manual_gear;
    public int manual_gear;
    public float steering;
    public float throttle;
}


public class show_objects : MonoBehaviour
{
	public GameObject stm_obj;
    public GameObject ai_obj;
    private int status = 0;
    private float x_angle = 45;
    private bool shown = false;
    public Vector3 a = new Vector3(0.0f, 0.0f, 0.0f);
    public Vector3 unity_rotation_vec = new Vector3(0.0f, 0.0f, 0.0f);


    // Start is called before the first frame update
    void Start()
    {
        stm_obj.SetActive(false);
        ai_obj.SetActive(true);
    }

    // Update is called once per frame
    void Update() {


        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(@"http://127.0.0.1:5000/hub/controlState");
        request.AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate;


        string response_string;
        try
        {
            using(HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using(Stream stream = response.GetResponseStream())
            using(StreamReader reader = new StreamReader(stream))
            {
                response_string = reader.ReadToEnd();
                Debug.Log(response_string);
                if(response_string == "AI"){
                    stm_obj.SetActive(false);
                    ai_obj.SetActive(true);
                }else if(response_string == "STM"){
                    stm_obj.SetActive(true);
                    ai_obj.SetActive(false);
                }
            }
        }catch(WebException ex){//če bomo kaj hendlali če ne dela 
        }

    }
}
