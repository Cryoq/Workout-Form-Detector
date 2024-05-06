    print("Realtime keypoints before scaling:", realtime_keypoints)

    try:
        # Print the shape of the realtime_keypoints array
        print("Realtime keypoints shape before scaling:", realtime_keypoints.shape)

        # Check if the scaler is fitted
        if scaler.n_samples_seen_ > 0:
            # Transform the real-time data using the fitted scaler
            realtime_keypoints_scaled = scaler.transform(realtime_keypoints)
            print("Realtime keypoints after scaling:", realtime_keypoints_scaled)
        else:
            print("Scaler has not been fitted yet.")
    except Exception as e:
        print("Error during scaling:", e)

    try:
        # Predict using the loaded model
        distance = loaded_model.predict(realtime_keypoints_scaled)
        print("Distance:", distance)
    except Exception as e:
        print("Error during prediction:", e)