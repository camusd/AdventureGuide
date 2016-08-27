package com.herokuapp.secret_bastion_27250.adventureguide;

import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.List;
import java.util.ArrayList;
import android.app.Activity;
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


public class CreateNewAccount extends ActionBarActivity {

    EditText user_id_field;
    EditText user_pw_field;
    EditText user_fname_field;
    EditText user_lname_field;
    EditText user_email_field;
    String user_id;
    String user_pw;
    String user_fname;
    String user_lname;
    String user_email;

    public static final String TAG_TOKEN = "token";
    public static final String TAG_USER = "newuser";
    public static final String MY_PREFS = "MyPrefsFile";
    public static final String URL = "http://secret-bastion-27250.herokuapp.com/api/users";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_new_account);

        user_id_field = (EditText) findViewById(R.id.adventure_guide_field_username);
        user_pw_field = (EditText) findViewById(R.id.adventure_guide_field_pw);
        user_fname_field = (EditText) findViewById(R.id.adventure_guide_field_fname);
        user_lname_field = (EditText) findViewById(R.id.adventure_guide_field_lname);
        user_email_field = (EditText) findViewById(R.id.adventure_guide_field_email);

        Button user_register_button = (Button) findViewById(R.id.adventure_guide_button_user_register);
        user_register_button.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View V) {
                // get data from form
                user_id = user_id_field.getText().toString();
                user_pw = user_pw_field.getText().toString();
                user_fname = user_fname_field.getText().toString();
                user_lname = user_lname_field.getText().toString();
                user_email = user_email_field.getText().toString();

                // add data to name-value pairs for POST form
                final List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
                nameValuePairs.add(new BasicNameValuePair("username", user_id));
                nameValuePairs.add(new BasicNameValuePair("password", user_pw));
                nameValuePairs.add(new BasicNameValuePair("firstname", user_fname));
                nameValuePairs.add(new BasicNameValuePair("lastname", user_lname));
                nameValuePairs.add(new BasicNameValuePair("email", user_email));

                // execute Async Task to post
                new MyAsyncTask().execute(nameValuePairs);
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_create_new_account, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    /* MyAsyncTask class is what will post form data to web service asynchronously */
    private class MyAsyncTask extends AsyncTask<List<NameValuePair>, Void, Void> {
        String response_string;
        int response_status;

        protected void onPostExecute(Void result) {
            Context context = getApplicationContext();

            CharSequence msg;
            if(response_status == 201) {
                msg = "Account Creation Successful";
            } else {
                msg = "Account Creation Error";
            }
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, msg, duration);
            toast.show();
        }
        protected Void doInBackground(List<NameValuePair>... nameValuePairs) {
            // get zero index of nameValuePairs
            List<NameValuePair> nvPairs = nameValuePairs[0];
            Log.i("nvPairs[0]", nameValuePairs[0].toString());
            InputStream inputStream = null;
            String postMessage= "{\"" + nvPairs.get(0).getName() + "\": \"" +
                    nvPairs.get(0).getValue() + "\", \"" + nvPairs.get(1).getName() + "\": \"" +
                    nvPairs.get(1).getValue() + "\", \"" + nvPairs.get(2).getName() + "\": \"" +
                    nvPairs.get(2).getValue() + "\", \"" + nvPairs.get(3).getName() + "\": \"" +
                    nvPairs.get(3).getValue() + "\", \"" + nvPairs.get(4).getName() + "\": \"" +
                    nvPairs.get(4).getValue() + "\"}";
            Log.i("postMessage", postMessage);
            try {
                HttpClient httpclient = new DefaultHttpClient();
                HttpPost myhttppost = new HttpPost(URL);
//                HttpPost myhttppost = new HttpPost("http://192.168.0.20:5000/api/users");
                myhttppost.setEntity(new ByteArrayEntity(postMessage.toString().getBytes("UTF8")));
                myhttppost.setHeader("Accept", "application/json");
                myhttppost.setHeader("Content-type", "application/json");
                HttpResponse response = httpclient.execute(myhttppost);
                inputStream = response.getEntity().getContent();
                response_string = convertInputStreamToString(inputStream);
                response_status = response.getStatusLine().getStatusCode();
                Log.i("postData", response_string);
                finish();

//                // parse the reply for token
//                if(response_string != null) {
//                    // parse the JSON
//                    try {
//                        JSONObject webserviceJSON = new JSONObject(response_string);
//                        Log.i("NewAccount", "JSON= " + webserviceJSON);
//
//                        // get the token
//                        String theToken = webserviceJSON.getString(TAG_TOKEN);
//                        String theUser = webserviceJSON.getString(TAG_USER);
//                        Log.i("NewAccount", "Parsed Token = " + theToken );
//
//                        // save whatever token and username in shared prefs
//                        SharedPreferences.Editor editor = getSharedPreferences(MY_PREFS, MODE_PRIVATE).edit();
//                        editor.putString("username", theUser);
//                        editor.putString("usertoken", theToken);
//                        editor.commit();
//                    } catch (JSONException e) {
//                        e.printStackTrace();
//                    }
//                }

            } catch (ClientProtocolException e) {
                // Log exception
                e.printStackTrace();
                //content.setText(e.toString());
            } catch (IOException e) {
                // Log exception
                e.printStackTrace();
                //content.setText(e.toString());
            }

            return null;

        }
    }

    private static String convertInputStreamToString(InputStream inputStream) throws IOException{
        // Credit: http://hmkcode.com/android-internet-connection-using-http-get-httpclient/
        BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(inputStream));
        String line = "";
        String result = "";
        while((line = bufferedReader.readLine()) != null)
            result += line;

        inputStream.close();
        return result;

    }
}