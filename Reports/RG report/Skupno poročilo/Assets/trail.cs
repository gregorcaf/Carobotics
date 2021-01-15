using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;//to 
using System.IO;//to
using System;

public partial class CarStateTrail
{
    public float speed;
    public int gear;
    public float rpm;
    public float maxrpm;
    public bool handbrake;
    public kinematics_estimated kinematic_estimated;
    public long timestamp;
}

public partial class kinematics_estimated
{
    public angular_acceleration position;
    public angular_acceleration orientation;
    public angular_acceleration linear_velocity;
    public angular_acceleration angular_velocity;
    public angular_acceleration linear_acceleration;
    public angular_acceleration angular_acceleration;
}

public partial class angular_acceleration
{
    public double x_val;
    public double y_val;
    public double z_val;
    public double? w_val;
}

public class trail : MonoBehaviour
{

	private int status = 0;
	private bool shown = false;
    public float hitrost = 0f;
    public Color trail_color = new Color(0.91f, 0.92f, 0.2f);
	TrailRenderer tr;


    void Start()
    {
        tr = GetComponent<TrailRenderer>();
        tr.startColor = trail_color;
        tr.endColor = trail_color;
        
    }

    // Update is called once per frame
    void Update() {

        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(@"http://127.0.0.1:5000/hub/CarState");
        string response_string;

        try
        {
            using(HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using(Stream stream = response.GetResponseStream())
            using(StreamReader reader = new StreamReader(stream))
            {
                response_string = reader.ReadToEnd();
                CarStateTrail car_state = (CarStateTrail)JsonUtility.FromJson(response_string, typeof(CarStateTrail));
                Debug.Log(car_state.speed);
                hitrost = car_state.speed;
                tr.startWidth = car_state.speed / 13;
                tr.endWidth = car_state.speed / 13;
            }
        }catch(WebException ex){//če bomo kaj hendlali če ne dela 
        }


        request = (HttpWebRequest)WebRequest.Create(@"http://127.0.0.1:5000/hub/getControl");

        try
        {
            using(HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            using(Stream stream = response.GetResponseStream())
            using(StreamReader reader = new StreamReader(stream))
            {
                response_string = reader.ReadToEnd();
                CarStateJson state = (CarStateJson)JsonUtility.FromJson(response_string, typeof(CarStateJson));
                Debug.Log(state.throttle);

                if (state.throttle >= 0) {
                    trail_color = new Color(0.91f, -0.7f * state.throttle + 0.9f, 0.2f);
                } else {
                    trail_color = new Color(0.91f, 0.92f, 0f);
                }


                tr.startColor = trail_color;
                tr.endColor = trail_color;
            }
        }catch(WebException ex){//če bomo kaj hendlali če ne dela 
        }







		// status++;
  //       if (status == 100) {
  //           shown = !shown;
  //           status = 0;
  //       }

  //       if (shown) {
	 //        tr.startColor = Color.red;
  //       	tr.endColor = Color.blue;
  //   	} else {
	 //        tr.startColor = Color.blue;
  //       	tr.endColor = Color.red;
  //   	}
    }
}
