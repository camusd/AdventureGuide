package com.herokuapp.secret_bastion_27250.adventureguide;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONStringer;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;


public class Login extends ActionBarActivity {

    EditText user_id_field;
    EditText user_pw_field;
    String user_id;
    String user_pw;

    public static final String TAG_TOKEN = "token";
    public static final String TAG_USER = "newUser";
    public static final String TAG_ID = "id";
    public static final String MY_PREFS = "MyPrefsFile";
    public static final String URL = "http://secret-bastion-27250.herokuapp.com/api/login";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        user_id_field = (EditText) findViewById(R.id.adventure_guide_field_username);
        user_pw_field = (EditText) findViewById(R.id.adventure_guide_field_pw);

        Button user_login_button = (Button) findViewById(R.id.adventure_guide_button_login);
        user_login_button.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View v) {
                user_id = user_id_field.getText().toString();
                user_pw = user_pw_field.getText().toString();
                final List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
                nameValuePairs.add(new BasicNameValuePair("userid", user_id));
                nameValuePairs.add(new BasicNameValuePair("userpw", user_pw));
                new MyAsyncTask().execute(nameValuePairs);
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            // add setting stuff here
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private class MyAsyncTask extends AsyncTask<List<NameValuePair>, Void, Void> {
        String response_string;
        int response_status;

        protected void onPostExecute(Void result) {
            Context context = getApplicationContext();

            CharSequence msg;
            if(response_status == 200) {
                msg = "Login Successful";
            } else {
                msg = "Incorrect Username or Password";
            }
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, msg, duration);
            toast.show();
        }

        protected Void doInBackground(List<NameValuePair>... nameValuePairs) {
            List<NameValuePair> nvPairs = nameValuePairs[0];
            Log.i("nvPairs[0]", nameValuePairs[0].toString());
            InputStream inputStream = null;
            String postMessage= "{\"" + nvPairs.get(0).getName() + "\": \"" +
                    nvPairs.get(0).getValue() + "\", \"" + nvPairs.get(1).getName() + "\": \"" +
                    nvPairs.get(1).getValue() + "\"}";
            Log.i("postMessage", postMessage);
            try {
                HttpClient httpclient = new DefaultHttpClient();
                HttpPost myhttppost = new HttpPost(URL);
//                HttpPost myhttppost = new HttpPost("http://192.168.0.20:5000/api/login");
                myhttppost.setEntity(new ByteArrayEntity(postMessage.toString().getBytes("UTF8")));
                myhttppost.setHeader("Accept", "application/json");
                myhttppost.setHeader("Content-type", "application/json");
                HttpResponse response = httpclient.execute(myhttppost);
                inputStream = response.getEntity().getContent();
                response_string = convertInputStreamToString(inputStream);
                response_status = response.getStatusLine().getStatusCode();
                inputStream.close();
                Log.i("postdata", response_string);
                if (response_string != null) {
                    try {
                        JSONObject webserviceJSON = new JSONObject(response_string);
                        Log.i("Login", "JSON=" + webserviceJSON);
                        String theToken = webserviceJSON.getString(TAG_TOKEN);
                        String theUser = webserviceJSON.getString(TAG_USER);
                        String theId = webserviceJSON.getString(TAG_ID);
                        Log.i("Login", "Parsed Token =" + theToken);
                        SharedPreferences.Editor editor = getSharedPreferences(MY_PREFS, MODE_PRIVATE).edit();
                        editor.putString("username", theUser);
                        editor.putString("usertoken", theToken);
                        editor.putString("id", theId);
                        editor.commit();
                        finish();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            } catch (ClientProtocolException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    private static String convertInputStreamToString(InputStream inputStream) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
        String line = "";
        String result = "";
        while((line = bufferedReader.readLine()) != null)
            result += line;
        inputStream.close();
        return result;
    }
}