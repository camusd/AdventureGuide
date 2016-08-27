package com.herokuapp.secret_bastion_27250.adventureguide;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

public class ViewReviews extends ActionBarActivity {

    public static final String MY_PREFS = "MyPrefsFile";

    String attraction;
    String name;
    CharSequence msg = "Sync complete";

    public static final String TAG_ITEM_USER = "username";
    public static final String TAG_ITEM_BODY = "body";
    public static final String TAG_ITEM_ID = "_id";

    public static String reviewURL = "http://secret-bastion-27250.herokuapp.com/api/majorAttractions/";
    ArrayList<HashMap<String, Object>> mylist = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_reviews);

        SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
        String theUser = prefs.getString("username", null);
        String theId = prefs.getString("id", null);

        // get extras from intent and populate view
        Intent myIntent = getIntent();
        attraction = myIntent.getStringExtra("attraction");
        name = myIntent.getStringExtra("name");
        TextView t = (TextView)findViewById(R.id.textView16);
        t.setText(name);

        // Test for network connection
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if(networkInfo != null && networkInfo.isConnected() ) {
            // we have network availability

            // get the JSON from Database
            new GetWebServiceData().execute();
        } else {
            // notify user of no network connection
            Context context = getApplicationContext();
            CharSequence msg = "No internet connection available, can not load data";
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, msg, duration);
            toast.show();
        }

        // Populate List View
        populateListView();

        // Register list click callback
        registerListClickCallback();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_view_reviews, menu);
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

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 0) {
            recreate();
        }

    }

    /**
     * Subclass GetWebServiceData uses HTTP Async Task to run on background thread.
     */
    private class GetWebServiceData extends AsyncTask<Void, Void, Void> {
        // help from http://www.androidhive.info/2012/01/android-json-parsing-tutorial/
        // and developer.android.com/training/basics/network-ops/connecting.html

        @Override
        protected Void doInBackground(Void... arg0) {

            try {
                // Get the information
                downloadUrl(reviewURL + attraction + "/reviews");
            } catch (IOException e) {
                // notify user of no network connection
                Context context = getApplicationContext();
                CharSequence msg = "Error: Unable to download from webservice";
                int duration = Toast.LENGTH_SHORT;
                Toast toast = Toast.makeText(context, msg, duration);
                toast.show();
            }

            return null;
        } /* End doInBackground */

        //onPostExecute dismisses the progress bar
        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);

            // notify user the sync is done
            Context context = getApplicationContext();
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, msg, duration);
            toast.show();
            populateListView();
        } /* onPostExecute */

        /** Given a URL, establishes a HttpUrlConnection and retrieves the content as an InputStream,
         * which it parses into the HashMap structure used to fill the ListView.
         */
        private void downloadUrl(String myUrl) throws IOException {
            InputStream is = null;
            String contentString = null;

            // retrieve from shared preferences
//            SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
//            final String theUser = prefs.getString("username", null);
//            final String theToken = prefs.getString("usertoken", null);

            // finish up building the url
//            myUrl += theUser;
//            myUrl += "/";
//            myUrl += theToken;
//
//            Log.d("myUrl", myUrl);

            java.net.URL url = new URL(myUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();

            try {
                // Set Timeouts
                conn.setReadTimeout(10000);
                conn.setConnectTimeout(15000);
                conn.setRequestMethod("GET");
                conn.setDoInput(true);
                // Start the query
                conn.connect();
                int response = conn.getResponseCode();
                if (response == 200) // if got actual data
                {
                    is = conn.getInputStream();
                    // Convert the InputStream into a string
                    contentString = InputStreamToString(is);
                }
                // Makes sure InputStream's closed & connection's disconnected after app's finished using it
            } finally {
                if (is != null) {
                    is.close();
                }
                conn.disconnect();
            }

            // Take the string that was returned and parse out component tables to make the HashMaps
            if (contentString != null) {
                Log.i("length", Integer.toString(contentString.length()));
                if (contentString.length() > 3) {
                    // Parse the JSON
                    try {
                        JSONArray webserviceJSON = new JSONArray(contentString);

                        // Loop the array (credit: http://mobile.dzone.com/news/android-tutorial-how-parse)
                        for (int i = 0; i < webserviceJSON.length(); i++) {
                            HashMap<String, Object> map = new HashMap<>();
                            JSONObject e = webserviceJSON.getJSONObject(i);
                            map.put(TAG_ITEM_BODY, e.getString(TAG_ITEM_BODY));
                            map.put(TAG_ITEM_USER, e.getString(TAG_ITEM_USER));
                            map.put(TAG_ITEM_ID, e.getString(TAG_ITEM_ID));
                            mylist.add(map);
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else {
                    msg = "No reviews found";
                }
            }

        } /* end DownloadURL() */

        public Bitmap LoadImage(String url) {
            try {
                InputStream is = new URL(url).openStream();
                Bitmap bitmap = BitmapFactory.decodeStream(is);
                is.close();
                return bitmap;
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

    } /* End GetWebService Data */

    public static String InputStreamToString(InputStream is1)  {
        BufferedReader rd = new BufferedReader(new InputStreamReader(is1), 4096);
        String line;
        StringBuilder sb =  new StringBuilder();
        try {
            while ((line = rd.readLine()) != null) {
                sb.append(line);
            }
            rd.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
        return sb.toString();
    } /* End InputStreamToString */

    SimpleAdapter.ViewBinder viewBinder = new SimpleAdapter.ViewBinder() {
        @Override
        public boolean setViewValue(View view, Object data, String textRep) {
            if (view.getId() == R.id.adventure_guide_item_user) {
                ((TextView)view).setText((String)data);
                return true;
            } else if (view.getId() == R.id.adventure_guide_item_body) {
                ((TextView)view).setText((String)data);
                return true;
            }
            return false;
        }
    };

    public void populateListView() {

        ListAdapter adapter = new SimpleAdapter(getApplicationContext(), mylist, R.layout.reviews_layout,
                new String[] {TAG_ITEM_USER,
                        TAG_ITEM_BODY},
                new int[] {R.id.adventure_guide_item_user,
                        R.id.adventure_guide_item_body}) {
            @Override
            public View getView(int position, View convertView, ViewGroup parent) {
                View view = super.getView(position, convertView, parent);
                view.setTag(mylist.get(position).get(TAG_ITEM_ID).toString());
                return view;
            }
        };

        // set the adapter for the list view
        ((SimpleAdapter)adapter).setViewBinder(viewBinder);
        ListView myList = (ListView)findViewById(R.id.listReviews);
        myList.setAdapter(adapter);
    }

    private void registerListClickCallback() {
        final ListView myList = (ListView) findViewById(R.id.listReviews);
        myList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View viewClicked,
                                    int position, long idInDB) {
                Intent reviewDetails = new Intent(ViewReviews.this, ViewReview.class);

                TextView tv_user = (TextView)viewClicked.findViewById(R.id.adventure_guide_item_user);
                TextView tv_body = (TextView)viewClicked.findViewById(R.id.adventure_guide_item_body);
                String str_user = tv_user.getText().toString();
                String str_body = tv_body.getText().toString();
                String str_id = viewClicked.getTag().toString();

                reviewDetails.putExtra("username", str_user);
                reviewDetails.putExtra("body", str_body);
                reviewDetails.putExtra("id", str_id);
                reviewDetails.putExtra("attraction", attraction);
                reviewDetails.putExtra("review_name", name);
                startActivityForResult(reviewDetails, 0);
            }
        });
    }
}
