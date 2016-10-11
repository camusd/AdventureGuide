package com.herokuapp.secret_bastion_27250.adventureguide;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class WriteReview extends ActionBarActivity {

    EditText edit_body_field;
    String attraction;
    String review_id;
    String body;
    String review_name;

    public static final String TAG_TOKEN = "token";
    public static final String TAG_USER = "newUser";
    public static final String TAG_ID = "id";
    public static final String MY_PREFS = "MyPrefsFile";
    public static final String URL = "http://secret-bastion-27250.herokuapp.com/api/reviews/";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_write_review);

        SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
        String theId = prefs.getString("id", null);

        Intent myIntent = getIntent();
        attraction = myIntent.getStringExtra("attraction");
        review_name = myIntent.getStringExtra("review_name");

        TextView t = (TextView)findViewById(R.id.textView21);
        t.setText(review_name);

        Button submit_button = (Button) findViewById(R.id.adventure_guide_button_submit2);
        submit_button.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View v) {
                SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
                String theId = prefs.getString("id", null);

                EditText body_field = (EditText) findViewById(R.id.adventure_guide_field_body);
                body = body_field.getText().toString();
                final List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
                nameValuePairs.add(new BasicNameValuePair("body", body));
                nameValuePairs.add(new BasicNameValuePair("attraction", attraction));
                nameValuePairs.add(new BasicNameValuePair("user", theId));

                new MyAsyncTask().execute(nameValuePairs);
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_write_review, menu);
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
            if(response_status == 201) {
                msg = "Review Submitted Successfully";
            } else if (response_status == 401){
                msg = "User credentials are invalid";
            } else {
                msg = "Session timed out";
            }
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, msg, duration);
            toast.show();
            finish();
        }

        protected Void doInBackground(List<NameValuePair>... nameValuePairs) {
            List<NameValuePair> nvPairs = nameValuePairs[0];
            Log.i("nvPairs[0]", nameValuePairs[0].toString());
            InputStream inputStream = null;
            String putMessage= "{\"" + nvPairs.get(0).getName() + "\": \"" +
                    nvPairs.get(0).getValue() + "\", \"" + nvPairs.get(1).getName() + "\": \"" +
                    nvPairs.get(1).getValue() + "\", \"" + nvPairs.get(2).getName() + "\": \"" +
                    nvPairs.get(2).getValue() + "\"}";
            Log.i("postMessage", putMessage);

            SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
            String theToken = prefs.getString("usertoken", null);
            String theId = prefs.getString("id", null);

            try {
                HttpClient httpclient = new DefaultHttpClient();
                HttpPost myhttppost = new HttpPost(URL + theId + "?token=" + theToken);
//                HttpPost myhttppost = new HttpPost("http://192.168.0.20:5000/api/login");
                myhttppost.setEntity(new ByteArrayEntity(putMessage.toString().getBytes("UTF8")));
                myhttppost.setHeader("Accept", "application/json");
                myhttppost.setHeader("Content-type", "application/json");
                HttpResponse response = httpclient.execute(myhttppost);
                inputStream = response.getEntity().getContent();
                response_string = convertInputStreamToString(inputStream);
                response_status = response.getStatusLine().getStatusCode();
                inputStream.close();
                Log.i("putdata", response_string);
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