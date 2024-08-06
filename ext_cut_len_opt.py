import streamlit as st
import math
import pandas as pd
 
# Function to calculate when Fab = "Y" and coring = "Y"
def Calculate_fab_Yes_coring_yes_No(total_order, weight_per_meter, cav, Adjusted_Butt_End, Die_type, Fab, coring):
    
    st.write("Enter Below Input Details")
    fab_cut = st.number_input("Enter fab cut length:", min_value=0.00000,format="%.5f")
    
    Machine_type = st.selectbox("Cutting machine type (Single head(1)/Double head(2))", [1, 2]) 
   
   
    number_of_nose_planned_list = []
   
    if Fab == "Y":
        number_of_nose_planned = 2  # Initialize number_of_nose_planned
       
        while True:
            if Machine_type == 1:
                Required_extrusion_cutlength = 15 + (fab_cut + 5) * number_of_nose_planned + 250
            elif Machine_type == 2:
                Required_extrusion_cutlength = 15 + ((15 + 5 + fab_cut + 5) * number_of_nose_planned)
            else:
                st.error("Enter Valid Machine Type")
                return
           
            if 3000 <= Required_extrusion_cutlength < 5500:
                number_of_nose_planned_list.append((number_of_nose_planned, Required_extrusion_cutlength))
            elif Required_extrusion_cutlength >= 5500:
                break
           
            number_of_nose_planned += 1
        selected_pair_index = st.selectbox("Possible Extrusion Cut Length:",options=range(len(number_of_nose_planned_list)),format_func=lambda idx: f"Fabrication Nose: {number_of_nose_planned_list[idx][0]}, Extrusion Length: {number_of_nose_planned_list[idx][1]}  mm")
           
       
       
   
    max_recovery = 0
    best_n = 0
    best_total_pcs_can_cut = 0  # Initialize to keep track of the best total_pcs_can_cut
    best_cut_length = 0
    best_number_of_nose_planned = 0
   
    if coring == "Y":
        results = []
       
        for number_of_nose_planned, Required_extrusion_cutlength in number_of_nose_planned_list:
            if Die_type == "H":
                for n in [580,650,725,830,965,1160]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    # Check if total_Ex_Length exceeds 48
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met
                   
                    front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300
                    back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                   
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    # st.write(f"total_pcs_cut{total_pcs_cut} Required_extrusion_cutlength{Required_extrusion_cutlength} best_n{Billet_size}")
       
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs} total available{total_leng_coring}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
                    # Special=(total_Ex_Weight*Billet_size*Total_No_of_Pcs_Mtrs*Recovery)/Excess_mtrs
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
                        best_cut_length = Required_extrusion_cutlength  # Store the best cut length
                        best_number_of_nose_planned = number_of_nose_planned  # Store the best number of nose planned
                        # st.write(f"best_cut_length{best_cut_length}")
                    
                   
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End (mm)':Adjusted_Butt_End,
                        'Extrudable Weight (Kg)':total_Ex_Weight,
                        'front_end (mtr)': front_end,
                        "back_end (mtr)": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery,
                        # "Special": Special
                    })
           
            elif Die_type == "S":
                for n in [580,650,725,830,965,1160]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met
                    front_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.3
                    back_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    # st.write(f"total_pcs_cut{total_pcs_cut}")
       
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
                    # Special=(total_Ex_Weight*Billet_size*Total_No_of_Pcs_Mtrs*Recovery)/Excess_mtrs
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
                        best_cut_length = Required_extrusion_cutlength  # Store the best cut length
                        best_number_of_nose_planned = number_of_nose_planned  # Store the best number of nose planned
                   
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End mm':Adjusted_Butt_End,
                        'Extrudable Weight Kg':total_Ex_Weight,
                        'front_end': front_end,
                        "back_end": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery,
                        # "Special": Special
                    })
           
            else:
                st.error("Input for Die type does not match")
   
    # else:
        # st.write("No input for Coring section.")
   
    # After finding the best_n and corresponding max_recovery, use them to calculate Total_billet_required
    if best_total_pcs_can_cut > 0:
        Total_billet_required = math.ceil(total_order / ((best_total_pcs_can_cut * best_number_of_nose_planned)*cav))
       
        # best_n is the last n in the loop
        Billet_size = best_n
        input_weight = Billet_size * 0.0876
        total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
        total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
        st.write(f"best_cut_length{best_cut_length}")
   
        # Calculate total length considering front and back end adjustments
        front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300 if Die_type == "H" else ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300
        back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav) if Die_type == "H" else ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
        # st.write(f"Front end coring:{front_end:.3f}")
        # st.write(f"Back end Coring:{back_end:.3f}")
       
        total_leng_coring = total_Ex_Length - (front_end + back_end)
        total_pcs_cut = math.floor(total_leng_coring / (best_cut_length / 1000))  # Use the best cut length for total_pcs_cut
        # st.write(f"total_pcs_cut{total_pcs_cut}")
       
        # Calculate output weight and recovery
        out_put = total_pcs_cut * ((best_cut_length*cav) / 1000) * weight_per_meter
        Total_output_weight = out_put * Total_billet_required
        Total_input_weight = Total_billet_required * Billet_size * 0.0876
   
        Total_recovery = (Total_output_weight / Total_input_weight) * 100

        Total_No_of_Pcs_Mtrs=(best_cut_length/1000)*total_pcs_cut
        Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
        # Special=(total_Ex_Weight*Billet_size*Total_No_of_Pcs_Mtrs*Total_recovery)/Excess_mtrs   
        # Create a DataFrame to store all results
        df_results = pd.DataFrame(results)
   
        # Print summary
        # st.subheader(f"Best Optimal Results")

        data = {
        "Parameter": [
        "Optimal Extrusion Cut Length",
        "Number of Fab Nose Planned in One Bar",
        "Maximum Recovery",
        "Billet Length",
        "Total Billets Required",
        "Total Input Weight",
        "Total Output Weight",
        "Total Recovery",
        "Total Extrudable Length per Billet mtr",
        "Front end coring mtr",
        "Back end Coring mtr"
                     ],
        "Value": [
        f"{best_cut_length} mm",
        f"{best_number_of_nose_planned:.0f} Nose",
        f"{max_recovery:.2f}%",
        f"{best_n} mm",
        f"{Total_billet_required} Nose",
        f"{Total_input_weight:.2f} kg",
        f"{Total_output_weight:.2f} kg",
        f"{Total_recovery:.2f}%",
        f"{total_Ex_Length:.3f} ",
        f"{front_end:3f}",
        f"{back_end:3f} "
            ]
        }

        # Create DataFrame
        df = pd.DataFrame(data)

        # Display table in Streamlit
        st.subheader("Best Optimal Results")
        st.write(df)

    
        # st.write(f"Optimal Extrusion cut length:  {best_cut_length} mm")
        # st.write(f"Number fab nose planned in one bar: {best_number_of_nose_planned:.0f} Nose")
        # st.write(f"Maximum Recovery: {max_recovery:.2f}%")
        # st.write(f"Billet Length: {best_n} Nose")
        # st.write(f"Total Billets Required: {Total_billet_required} Nose")
        # st.write(f"Total Input Weight: {Total_input_weight:.2f} kg")
        # st.write(f"Total Output Weight: {Total_output_weight:.2f} kg")
        # st.write(f"Total Recovery: {Total_recovery:.2f}%")       
        # st.write(f"Total extrudable length per billet: {total_Ex_Length:.3f} Meter")
 
        # Filter df_results to show only the results for the best_cut_length
        best_n_values = [580, 650, 725, 830, 965, 1160]
        Billets = st.selectbox("Select Billet cut length to check recovery for other billets:", best_n_values)
       
        filtered_results = df_results[df_results['Billet Length (mm)'] == Billets]

        def highlight_max_adjust(row):
            return ['background-color: lightgreen' if row.name == filtered_results["Recovery"].idxmax() else '' for _ in row]

        # Apply the highlighting function and display DataFrame
        st.write("Results with highlighted row for maximum Adjust value:")
        st.dataframe(filtered_results.style.apply(highlight_max_adjust, axis=1))
   
        # # Display the filtered results DataFrame
        # st.write("\nResults for selected billet length with fab passible cut_length:")
        # st.dataframe(filtered_results)

        st.write("\nUse when you can adjust coring tolerance less than 0.25 mtr:")
        df_new=df_results
        df_new["Adjust"]=(df_new["Excess mtrs"]-(df_new["Cut_length"]/1000))
        df_new["updated_No_of_pcs_to_plan"]=df_new["No_of_Pcs_to_plan"]+1
        out_put = df_new["updated_No_of_pcs_to_plan"] * ((df_new["Cut_length"]*cav) / 1000) * weight_per_meter
        Total_input_weight=df_new["Billet Length (mm)"]*0.0876
        df_new["Adjusted_recovery"]=(out_put/Total_input_weight)*100
        best_n_values1 = [580, 650, 725, 830, 965, 1160]
        Billets1 = st.selectbox("Enter Required billet size:", best_n_values1)
        # best_cut_length1 = st.selectbox("Select Billet cut length to check recovery for other billets:", [x[1] for x in number_of_nose_planned_list])
        df_new = df_new[df_new['Billet Length (mm)'] == Billets1]
        df_new_sort=df_new.sort_values(by="Adjust",ascending=False)

        def highlight_max_adjust(row):
            return ['background-color: lightgreen' if row.name == df_new_sort["Adjust"].idxmax() else '' for _ in row]

        # Apply the highlighting function and display DataFrame
        st.write("Results with highlighted row for maximum Adjust value:")
        st.dataframe(df_new_sort.style.apply(highlight_max_adjust, axis=1))

           
    max_recovery = 0
    best_n = 0
    best_total_pcs_can_cut = 0  # Initialize to keep track of the best total_pcs_can_cut
    best_cut_length = 0
   
    if coring == "N":
        Stretch_Allowance = st.number_input("Enter Stretch_Allowance if no coring (mtr):", min_value=0.001, step=0.001, format="%.5f")
        results = []
        for number_of_nose_planned, Required_extrusion_cutlength in number_of_nose_planned_list:
            for n in range(500,1201,5):  # Iterate through n values 5, 6, 7, 8, 9
                Billet_size = n
                input_weight = Billet_size * 0.0876
                total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                total_Ex_Length = (total_Ex_Weight / (weight_per_meter * cav))+0 # +2 is for stretching allowance
                if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met
                

                total_pcs_can_cut = math.floor((total_Ex_Length-Stretch_Allowance) / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                # st.write(f"total_pcs_can_cut{total_pcs_can_cut} Required_extrusion_cutlength{Required_extrusion_cutlength} best_n{Billet_size}")
               
                # Calculate output weight and recovery
                out_put = total_pcs_can_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                Recovery = (out_put / input_weight) * 100
                Total_No_of_Pcs_Mtrs=total_pcs_can_cut*(Required_extrusion_cutlength/1000)
                Excess_mtrs=total_Ex_Length-Total_No_of_Pcs_Mtrs
       
                # Check if this recovery is the maximum so far
                if Recovery > max_recovery:
                    max_recovery = Recovery
                    best_n = n
                    best_total_pcs_can_cut = total_pcs_can_cut  # Update best total_pcs_can_cut
                    best_cut_length = Required_extrusion_cutlength  # Update best cut length
                    best_number_of_nose_planned=number_of_nose_planned
                    # st.write(f"best_cut_length{best_cut_length}")
       
                # Collect results for each n and cut length
                results.append({
                    'Billet Length (mm)': n,
                    'Butt End mm':Adjusted_Butt_End,
                    'Extrudable Weight Kg':total_Ex_Weight,
                    'Total mtrs':total_Ex_Length,             
                    'No_of_Pcs_to_plan': total_pcs_can_cut,
                    'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                    'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                    'Excess mtrs':Excess_mtrs,                        
                    'Recovery': Recovery
                })
       
        # After finding the best_n, best_cut_length, and corresponding max_recovery, use them to calculate Total_billet_required
        if best_total_pcs_can_cut > 0:
            Total_billet_required = math.ceil(total_order / ((best_total_pcs_can_cut * best_number_of_nose_planned)*cav))
            Billet_size=best_n
            input_weight=Billet_size*0.0876
            total_Ex_Weight=(Billet_size-Adjusted_Butt_End)*0.0876
            total_Ex_Length=total_Ex_Weight/(weight_per_meter*cav)

            total_pcs_can_cut=math.floor(total_Ex_Length/(best_cut_length/1000))
            out_put = total_pcs_can_cut * ((best_cut_length*cav) / 1000) * weight_per_meter 
            Total_output_weight = Total_billet_required * out_put        


            Total_input_weight = Total_billet_required *  Billet_size * 0.0876
            
            
            Total_recovery = (Total_output_weight / Total_input_weight) * 100
            st.write(f"best_cut_length{best_cut_length}")
   
            # Create a DataFrame to store all results
            df_results = pd.DataFrame(results)
   
            # Print summary
            data = {
        "Parameter": [
        "Optimal Extrusion Cut Length",
        "Number of Fab Nose Planned in One Bar",
        "Maximum Recovery",
        "Billet Length",
        "Total Billets Required",
        "Total Input Weight",
        "Total Output Weight",
        "Total Recovery",
        "Total Extrudable Length per Billet"
                     ],
        "Value": [
        f"{best_cut_length} mm",
        f"{best_number_of_nose_planned:.0f} Nose",
        f"{max_recovery:.2f}%",
        f"{best_n} mm",
        f"{Total_billet_required} Nose",
        f"{Total_input_weight:.2f} kg",
        f"{Total_output_weight:.2f} kg",
        f"{Total_recovery:.2f}%",
        f"{total_Ex_Length:.3f} Meter"
            ]
        }

            # Create DataFrame
            df = pd.DataFrame(data)

            # Display table in Streamlit
            st.subheader("Best Optimal Results")
            st.write(df)
            # st.subheader(f"Best Optimal Results")
            # st.write(f"Optimal Extrusion cut length = {best_cut_length} mm")
            # st.write(f"Maximum Recovery: {max_recovery:.2f}% ")
            # st.write(f"Billet Length: {best_n} Nose")
            # st.write(f"Total Billets Required: {Total_billet_required} Nose")
            # st.write(f"Total Input Weight: {Total_input_weight:.2f} kg")
            # st.write(f"Total Output Weight: {Total_output_weight:.2f} kg")
            # st.write(f"Total Recovery: {Total_recovery:.2f}%")
            # st.write(f"Total extrudable length:{total_Ex_Length:.3f} Meter")
   
            # Display the DataFrame filtered for the best results
            
            Billets = st.number_input("Enter Billet Length (mm):", min_value=500.00,step=5.00,format="%.3f")
            best_results = df_results[(df_results['Billet Length (mm)'] == Billets)]
            def highlight_max_adjust(row):
                return ['background-color: lightgreen' if row.name == best_results["Recovery"].idxmax() else '' for _ in row]

            # Apply the highlighting function and display DataFrame
            st.write("Results with highlighted row for maximum Adjust value:")
            st.dataframe(best_results.style.apply(highlight_max_adjust, axis=1))

   
        else:
            st.write("No valid total_pcs_can_cut found.")


# Function to calculate when Fab = "Y" and coring = "Y"
def Calculate_fab_Yes_coring_yes_No_press1(total_order, weight_per_meter, cav, Adjusted_Butt_End, Die_type, Fab, coring):
   
    st.write("Enter Below Input Details")
    fab_cut = st.number_input("Enter fab cut length:", min_value=0.00000,format="%.5f")
    
    Machine_type = st.selectbox("Cutting machine type (Single head(1)/Double head(2))", [1, 2]) 
   
   
    number_of_nose_planned_list = []
   
    if Fab == "Y":
        number_of_nose_planned = 2  # Initialize number_of_nose_planned
       
        while True:
            if Machine_type == 1:
                Required_extrusion_cutlength = 15 + (fab_cut + 5) * number_of_nose_planned + 250
            elif Machine_type == 2:
                Required_extrusion_cutlength = 15 + ((15 + 5 + fab_cut + 5) * number_of_nose_planned)
            else:
                st.error("Enter Valid Machine Type")
                return
           
            if 3000 <= Required_extrusion_cutlength < 5500:
                number_of_nose_planned_list.append((number_of_nose_planned, Required_extrusion_cutlength))
            elif Required_extrusion_cutlength >= 5500:
                break
           
            number_of_nose_planned += 1
        selected_pair_index = st.selectbox("Possible Extrusion Cut Length:",options=range(len(number_of_nose_planned_list)),format_func=lambda idx: f"Fabrication Nose: {number_of_nose_planned_list[idx][0]}, Extrusion Length: {number_of_nose_planned_list[idx][1]}  mm")
           
       
       
   
    max_recovery = 0
    best_n = 0
    best_total_pcs_can_cut = 0  # Initialize to keep track of the best total_pcs_can_cut
    best_cut_length = 0
    best_number_of_nose_planned = 0
   
    if coring == "Y":
        results = []
       
        for number_of_nose_planned, Required_extrusion_cutlength in number_of_nose_planned_list:
            if Die_type == "H":
                for n in [580,650,725,830,965]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    # Check if total_Ex_Length exceeds 48
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met
                   
                    front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300
                    back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                   
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    # st.write(f"total_pcs_cut{total_pcs_cut} Required_extrusion_cutlength{Required_extrusion_cutlength} best_n{Billet_size}")
       
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs} total available{total_leng_coring}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
                        best_cut_length = Required_extrusion_cutlength  # Store the best cut length
                        best_number_of_nose_planned = number_of_nose_planned  # Store the best number of nose planned
                        # st.write(f"best_cut_length{best_cut_length}")
                   
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End mm':Adjusted_Butt_End,
                        'Extrudable Weight Kg':total_Ex_Weight,
                        'front_end': front_end,
                        "back_end": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery
                    })
           
            elif Die_type == "S":
                for n in [580,650,725,830,965]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met
                    front_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.3
                    back_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    # st.write(f"total_pcs_cut{total_pcs_cut}")
       
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
                        best_cut_length = Required_extrusion_cutlength  # Store the best cut length
                        best_number_of_nose_planned = number_of_nose_planned  # Store the best number of nose planned
                   
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End mm':Adjusted_Butt_End,
                        'Extrudable Weight Kg':total_Ex_Weight,
                        'front_end': front_end,
                        "back_end": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery
                    })
           
            else:
                st.error("Input for Die type does not match")
   
    # else:
        # st.write("No input for Coring section.")
   
    # After finding the best_n and corresponding max_recovery, use them to calculate Total_billet_required
    if best_total_pcs_can_cut > 0:
        Total_billet_required = math.ceil(total_order / ((best_total_pcs_can_cut * best_number_of_nose_planned)*cav))
       
        # best_n is the last n in the loop
        Billet_size = best_n
        input_weight = Billet_size * 0.0876
        total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
        total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
        st.write(f"best_cut_length{best_cut_length}")
   
        # Calculate total length considering front and back end adjustments
        front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300 if Die_type == "H" else ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300
        back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav) if Die_type == "H" else ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
       
        total_leng_coring = total_Ex_Length - (front_end + back_end)
        total_pcs_cut = math.floor(total_leng_coring / (best_cut_length / 1000))  # Use the best cut length for total_pcs_cut
        # st.write(f"total_pcs_cut{total_pcs_cut}")
       
        # Calculate output weight and recovery
        out_put = total_pcs_cut * ((best_cut_length*cav) / 1000) * weight_per_meter
        Total_output_weight = out_put * Total_billet_required
        Total_input_weight = Total_billet_required * Billet_size * 0.0876
   
        Total_recovery = (Total_output_weight / Total_input_weight) * 100
   
        # Create a DataFrame to store all results
        df_results = pd.DataFrame(results)
   
        # Print summary
        # st.subheader(f"Best Optimal Results")

        data = {
        "Parameter": [
        "Optimal Extrusion Cut Length",
        "Number of Fab Nose Planned in One Bar",
        "Maximum Recovery",
        "Billet Length",
        "Total Billets Required",
        "Total Input Weight",
        "Total Output Weight",
        "Total Recovery",
        "Total Extrudable Length per Billet mtr",
        "Front end coring mtr",
        "Back end coring mtr"
                     ],
        "Value": [
        f"{best_cut_length} mm",
        f"{best_number_of_nose_planned:.0f} Nose",
        f"{max_recovery:.2f}%",
        f"{best_n} mm",
        f"{Total_billet_required} Nose",
        f"{Total_input_weight:.2f} kg",
        f"{Total_output_weight:.2f} kg",
        f"{Total_recovery:.2f}%",
        f"{total_Ex_Length:.3f}",
        f"{front_end:.3f}",
        f"{back_end:.3f}"
            ]
        }

        # Create DataFrame
        df = pd.DataFrame(data)

        # Display table in Streamlit
        st.subheader("Best Optimal Results")
        st.write(df)

        # st.write(f"Optimal Extrusion cut length:  {best_cut_length} mm")
        # st.write(f"Number fab nose planned in one bar: {best_number_of_nose_planned:.0f} Nose")
        # st.write(f"Maximum Recovery: {max_recovery:.2f}%")
        # st.write(f"Billet Length: {best_n} Nose")
        # st.write(f"Total Billets Required: {Total_billet_required} Nose")
        # st.write(f"Total Input Weight: {Total_input_weight:.2f} kg")
        # st.write(f"Total Output Weight: {Total_output_weight:.2f} kg")
        # st.write(f"Total Recovery: {Total_recovery:.2f}%")       
        # st.write(f"Total extrudable length per billet: {total_Ex_Length:.3f} Meter")
 
        # Filter df_results to show only the results for the best_cut_length
        best_n_values = [580, 650, 725, 830, 965, 1160]
        Billets = st.selectbox("Select Billet cut length to check recovery for other billets:", best_n_values)
       
        filtered_results = df_results[df_results['Billet Length (mm)'] == Billets]
        def highlight_max_adjust(row):
            return ['background-color: lightgreen' if row.name == filtered_results["Recovery"].idxmax() else '' for _ in row]

        # Apply the highlighting function and display DataFrame
        st.write("Results with highlighted row for maximum Adjust value:")
        st.dataframe(filtered_results.style.apply(highlight_max_adjust, axis=1))
   
        

        
        st.write("\nUse when you can adjust coring tolerance less than 0.25 mtr:")
        df_new=df_results
        df_new["Adjust"]=(df_new["Excess mtrs"]-(df_new["Cut_length"]/1000))
        df_new["updated_No_of_pcs_to_plan"]=df_new["No_of_Pcs_to_plan"]+1
        out_put = df_new["updated_No_of_pcs_to_plan"] * ((df_new["Cut_length"]*cav) / 1000) * weight_per_meter
        Total_input_weight=df_new["Billet Length (mm)"]*0.0876
        df_new["Adjusted_recovery"]=(out_put/Total_input_weight)*100
        best_n_values1 = [580, 650, 725, 830, 965, 1160]
        Billets1 = st.selectbox("Enter Required billet size:", best_n_values1)
        # best_cut_length1 = st.selectbox("Select Billet cut length to check recovery for other billets:", [x[1] for x in number_of_nose_planned_list])
        df_new = df_new[df_new['Billet Length (mm)'] == Billets1]
        df_new_sort=df_new.sort_values(by="Adjust",ascending=False)

        def highlight_max_adjust(row):
            return ['background-color: lightgreen' if row.name == df_new_sort["Adjust"].idxmax() else '' for _ in row]

        # Apply the highlighting function and display DataFrame
        st.write("Results with highlighted row for maximum Adjust value:")
        st.dataframe(df_new_sort.style.apply(highlight_max_adjust, axis=1))
   
    max_recovery = 0
    best_n = 0
    best_total_pcs_can_cut = 0  # Initialize to keep track of the best total_pcs_can_cut
    best_cut_length = 0
   
    if coring == "N":
        Stretch_Allowance = st.number_input("Enter Stretch_Allowance if no coring (mtr):", min_value=0.001, step=0.001, format="%.5f")
        results = []
        for number_of_nose_planned, Required_extrusion_cutlength in number_of_nose_planned_list:
            for n in range(500,1001,5):  # Iterate through n values 5, 6, 7, 8, 9
                Billet_size = n
                input_weight = Billet_size * 0.0876
                total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                total_Ex_Length = (total_Ex_Weight / (weight_per_meter * cav))+0 # +2 is for stretching allowance
                if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met
                

                total_pcs_can_cut = math.floor((total_Ex_Length-Stretch_Allowance) / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                # st.write(f"total_pcs_can_cut{total_pcs_can_cut} Required_extrusion_cutlength{Required_extrusion_cutlength} best_n{Billet_size}")
               
                # Calculate output weight and recovery
                out_put = total_pcs_can_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                Recovery = (out_put / input_weight) * 100
                Total_No_of_Pcs_Mtrs=total_pcs_can_cut*(Required_extrusion_cutlength/1000)
                Excess_mtrs=total_Ex_Length-Total_No_of_Pcs_Mtrs
       
                # Check if this recovery is the maximum so far
                if Recovery > max_recovery:
                    max_recovery = Recovery
                    best_n = n
                    best_total_pcs_can_cut = total_pcs_can_cut  # Update best total_pcs_can_cut
                    best_cut_length = Required_extrusion_cutlength  # Update best cut length
                    best_number_of_nose_planned=number_of_nose_planned
                    # st.write(f"best_cut_length{best_cut_length}")
       
                # Collect results for each n and cut length
                results.append({
                    'Billet Length (mm)': n,
                    'Butt End mm':Adjusted_Butt_End,
                    'Extrudable Weight Kg':total_Ex_Weight,
                    'Total mtrs':total_Ex_Length,             
                    'No_of_Pcs_to_plan': total_pcs_can_cut,
                    'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                    'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                    'Excess mtrs':Excess_mtrs,                        
                    'Recovery': Recovery
                })
       
        # After finding the best_n, best_cut_length, and corresponding max_recovery, use them to calculate Total_billet_required
        if best_total_pcs_can_cut > 0:
            Total_billet_required = math.ceil(total_order / ((best_total_pcs_can_cut * best_number_of_nose_planned)*cav))
            Billet_size=best_n
            input_weight=Billet_size*0.0876
            total_Ex_Weight=(Billet_size-Adjusted_Butt_End)*0.0876
            total_Ex_Length=total_Ex_Weight/(weight_per_meter*cav)

            total_pcs_can_cut=math.floor(total_Ex_Length/(best_cut_length/1000))
            out_put = total_pcs_can_cut * ((best_cut_length*cav) / 1000) * weight_per_meter 
            Total_output_weight = Total_billet_required * out_put        


            Total_input_weight = Total_billet_required *  Billet_size * 0.0876
            
            
            Total_recovery = (Total_output_weight / Total_input_weight) * 100
            st.write(f"best_cut_length{best_cut_length}")
   
            # Create a DataFrame to store all results
            df_results = pd.DataFrame(results)
   
            # Print summary
            data = {
        "Parameter": [
        "Optimal Extrusion Cut Length",
        "Number of Fab Nose Planned in One Bar",
        "Maximum Recovery",
        "Billet Length",
        "Total Billets Required",
        "Total Input Weight",
        "Total Output Weight",
        "Total Recovery",
        "Total Extrudable Length per Billet"
                     ],
        "Value": [
        f"{best_cut_length} mm",
        f"{best_number_of_nose_planned:.0f} Nose",
        f"{max_recovery:.2f}%",
        f"{best_n} mm",
        f"{Total_billet_required} Nose",
        f"{Total_input_weight:.2f} kg",
        f"{Total_output_weight:.2f} kg",
        f"{Total_recovery:.2f}%",
        f"{total_Ex_Length:.3f} Meter"
            ]
        }

            # Create DataFrame
            df = pd.DataFrame(data)

            # Display table in Streamlit
            st.subheader("Best Optimal Results")
            st.write(df)
            # st.subheader(f"Best Optimal Results")
            # st.write(f"Optimal Extrusion cut length = {best_cut_length} mm")
            # st.write(f"Maximum Recovery: {max_recovery:.2f}% ")
            # st.write(f"Billet Length: {best_n} Nose")
            # st.write(f"Total Billets Required: {Total_billet_required} Nose")
            # st.write(f"Total Input Weight: {Total_input_weight:.2f} kg")
            # st.write(f"Total Output Weight: {Total_output_weight:.2f} kg")
            # st.write(f"Total Recovery: {Total_recovery:.2f}%")
            # st.write(f"Total extrudable length:{total_Ex_Length:.3f} Meter")
   
            # Display the DataFrame filtered for the best results
            
            Billets = st.number_input("Enter Billet Length (mm):", min_value=500.00,step=5.00,format="%.3f")
            best_results = df_results[(df_results['Billet Length (mm)'] == Billets)]
            def highlight_max_adjust(row):
                return ['background-color: lightgreen' if row.name == best_results["Recovery"].idxmax() else '' for _ in row]

            # Apply the highlighting function and display DataFrame
            st.write("Results with highlighted row for maximum Adjust value:")
            st.dataframe(best_results.style.apply(highlight_max_adjust, axis=1))
   
   
        else:
            st.write("No valid total_pcs_can_cut found.")



def calculate_recovery_Fab_No_coring_Yes_No(Die_Number, weight_per_meter, cav, cut_length, total_order, Adjusted_Butt_End, Fab, coring, Die_type):
    
    max_recovery = 0
    best_n = 0
    best_total_pcs_can_cut = 0  # Initialize to keep track of the best total_pcs_can_cut
    Required_extrusion_cutlength = cut_length
   
    # Check if Fab is "N"
    if Fab == "N":
        results = []
        # Check if Coring is "Y"
        if coring == "Y":
            if Die_type == "H":
                for n in [580,650,725,830,965,1160]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met

                    front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300
                    back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                   
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
                           
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
       
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End mm':Adjusted_Butt_End,
                        'Extrudable Weight Kg':total_Ex_Weight,
                        'front_end': front_end,
                        "back_end": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery
                    })
       
            elif Die_type == "S":
                for n in [580,650,725,830,965,1160]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met

                    front_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.3
                    back_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                   
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
                   
       
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
       
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End mm':Adjusted_Butt_End,
                        'Extrudable Weight Kg':total_Ex_Weight,
                        'front_end': front_end,
                        "back_end": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery
                    })
       
            else:
                st.error("No input for Die type")
                return
       
            # After finding the best_n and corresponding max_recovery, use them to calculate Total_billet_required
            if best_total_pcs_can_cut > 0:
                Total_billet_required = math.ceil(total_order / (best_total_pcs_can_cut*cav))

                Billet_size = best_n
                input_weight = Billet_size * 0.0876
                total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)

               
                front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300 if Die_type == "H" else ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300
                back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav) if Die_type == "H" else ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
               
                total_leng_coring = total_Ex_Length - (front_end + back_end)
                total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))
       
                out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                Total_output_weight = out_put * Total_billet_required
                Total_input_weight = Total_billet_required * Billet_size * 0.0876
       
                Total_recovery = (Total_output_weight / Total_input_weight) * 100
       
                df_results = pd.DataFrame(results)

                data = {
                "Parameter": [
                
                "Maximum Recovery",
                "Billet Length",
                "Total Billets Required",
                "Total Input Weight",
                "Total Output Weight",
                "Total Recovery",
                "Total Extrudable Length per Billet mtr",
                "Front end coring mtr",
                "Back end coring mtr"
                     ],
                "Value": [
                
                f"{max_recovery:.2f}%",
                f"{best_n} mm",
                f"{Total_billet_required} Nose",
                f"{Total_input_weight:.2f} kg",
                f"{Total_output_weight:.2f} kg",
                f"{Total_recovery:.2f}%",
                f"{total_Ex_Length:.3f} Meter",
                f"{front_end:.3f}",
                f"{back_end:.3f}"
                    ]
                }

                # Create DataFrame
                df = pd.DataFrame(data)

                # Display table in Streamlit
                st.subheader("Best Optimal Results")
                st.write(df)
                # st.subheader(f"Best Optimal Results")        
                # st.write(f"Maximum Recovery: {max_recovery:.2f}% with n = {best_n}")
                # st.write(f"Total Billets Required: {Total_billet_required}")
                # st.write(f"Total Input Weight: {Total_input_weight:.3f} kg")
                # st.write(f"Total Output Weight: {Total_output_weight:.3f} kg")
                # st.write(f"Total Recovery: {Total_recovery:.3f}%")
       
                st.subheader("Results for each Billet")

                def highlight_max_adjust(row):
                    return ['background-color: lightgreen' if row.name == df_results["Recovery"].idxmax() else '' for _ in row]

                # Apply the highlighting function and display DataFrame
                st.write("Results with highlighted row for maximum Adjust value:")
                st.dataframe(df_results.style.apply(highlight_max_adjust, axis=1))

                

                st.write("\nUse when you can adjust coring tolerance less than 0.25 mtr:")
                df_new=df_results
                df_new["Adjust"]=(df_new["Excess mtrs"]-(df_new["Cut_length"]/1000))
                df_new["updated_No_of_pcs_to_plan"]=df_new["No_of_Pcs_to_plan"]+1
                out_put = df_new["updated_No_of_pcs_to_plan"] * ((df_new["Cut_length"]*cav) / 1000) * weight_per_meter
                Total_input_weight=df_new["Billet Length (mm)"]*0.0876
                df_new["Adjusted_recovery"]=(out_put/Total_input_weight)*100
                # df_new = df_new[df_new['Cut_length'] == best_cut_length]
                df_new_sort=df_new.sort_values(by="Adjust",ascending=False)

                def highlight_max_adjust(row):
                    return ['background-color: lightgreen' if row.name == df_new_sort["Adjust"].idxmax() else '' for _ in row]

                # Apply the highlighting function and display DataFrame
                st.write("Results with highlighted row for maximum Adjust value:")
                st.dataframe(df_new_sort.style.apply(highlight_max_adjust, axis=1))


                
       
            
       
        elif coring == "N":
            Stretch_Allowance = st.number_input("Enter Stretch_Allowance if no coring (mtr):", min_value=0.001, step=0.001, format="%.5f")
            results = []
            for n in range(500,1201,5):  # Iterate through n values 5, 6, 7, 8, 9
                Billet_size = n
                input_weight = Billet_size * 0.0876
                total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)+0 #+2 is for stretching allowance
                if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met               
                

                total_pcs_can_cut = math.floor((total_Ex_Length-Stretch_Allowance) / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
               
                # Calculate output weight and recovery
                out_put = total_pcs_can_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                Recovery = (out_put / input_weight) * 100
                Total_No_of_Pcs_Mtrs=total_pcs_can_cut*(Required_extrusion_cutlength/1000)
                Excess_mtrs=total_Ex_Length-Total_No_of_Pcs_Mtrs
       
                # Check if this recovery is the maximum so far
                if Recovery > max_recovery:
                    max_recovery = Recovery
                    best_n = n
                    best_total_pcs_can_cut = total_pcs_can_cut  # Update best total_pcs_can_cut
       
                # Collect results for each n
                results.append({
                    'Billet Length (mm)': n,
                    'Butt End mm':f"{Adjusted_Butt_End:.2f}",
                    'Extrudable Weight Kg':f"{total_Ex_Weight:.2f}",
                    'Total mtrs':f"{total_Ex_Length:.2f}",             
                    'No_of_Pcs_to_plan': total_pcs_can_cut,
                    'Total No of Pcs Mtrs':f"{Total_No_of_Pcs_Mtrs:.2f}",
                    'Cut_length': f"{Required_extrusion_cutlength:.2f}",  # Store the cut length in results
                    'Excess mtrs':f"{Excess_mtrs:.2f}",                        
                    'Recovery': f"{Recovery:.2f} %"
                })
       
            # After finding the best_n and corresponding max_recovery, use them to calculate Total_billet_required
            if best_total_pcs_can_cut > 0:
                Total_billet_required = math.ceil(total_order / (best_total_pcs_can_cut*cav))

                Billet_size = best_n
                input_weight=Billet_size*0.0876
                total_Ex_Weight=(Billet_size-Adjusted_Butt_End)*0.0876
                total_Ex_Length=total_Ex_Weight/(weight_per_meter*cav)

                total_pcs_can_cut=math.floor(total_Ex_Length/(Required_extrusion_cutlength/1000))

                out_put=total_pcs_can_cut*((Required_extrusion_cutlength*cav)/1000)*weight_per_meter
                Total_output_weight = Total_billet_required * out_put
                Total_input_weight = (Total_billet_required * (Billet_size)) * 0.0876
                Total_recovery = (Total_output_weight / Total_input_weight) * 100
       
                df_results = pd.DataFrame(results)

                data = {
                "Parameter": [
                
                "Maximum Recovery",
                "Billet Length",
                "Total Billets Required",
                "Total Input Weight",
                "Total Output Weight",
                "Total Recovery",
                "Total Extrudable Length per Billet"
                     ],
                "Value": [
                
                f"{max_recovery:.2f}%",
                f"{best_n} mm",
                f"{Total_billet_required} Nose",
                f"{Total_input_weight:.2f} kg",
                f"{Total_output_weight:.2f} kg",
                f"{Total_recovery:.2f}%",
                f"{total_Ex_Length:.3f} Meter"
                    ]
                }

                # Create DataFrame
                df = pd.DataFrame(data)

                # Display table in Streamlit
                st.subheader("Best Optimal Results")
                st.write(df)
                # st.subheader(f"Best Optimal Results")
                # st.write(f"Maximum Recovery: {max_recovery:.3f}% with n = {best_n}")
                # st.write(f"Total Billets Required: {Total_billet_required}")
                # st.write(f"Total Input Weight: {Total_input_weight:.3f} kg")
                # st.write(f"Total Output Weight: {Total_output_weight:.3f} kg")
                # st.write(f"Total Recovery: {Total_recovery:.3f}%")
               
       
                # st.subheader("Results for each Billet")
                Billets = st.number_input("Enter Billet Length (mm):", min_value=500.00,step=5.00,format="%.3f")
                df_results = df_results[(df_results['Billet Length (mm)'] == Billets)]
                st.write("\nResults for selected billet length with fab passible cut_length:")
                def highlight_lowest_adjust(row):
                    return ['background-color: lightgreen' if val == df_results["Recovery"].max() else '' for val in row]

                # Apply the highlighting function and display DataFrame
                
                st.dataframe(df_results.style.apply(highlight_lowest_adjust, axis=1))
                
       
            else:
                st.warning("No valid total_pcs_can_cut found.")
   
    else:
        st.error("Enter valid details for Fabrication Required")




def calculate_recovery_Fab_No_coring_Yes_No_press1(Die_Number, weight_per_meter, cav, cut_length, total_order, Adjusted_Butt_End, Fab, coring, Die_type):
    
    max_recovery = 0
    best_n = 0
    best_total_pcs_can_cut = 0  # Initialize to keep track of the best total_pcs_can_cut
    Required_extrusion_cutlength = cut_length
   
    # Check if Fab is "N"
    if Fab == "N":
        results = []
        # Check if Coring is "Y"
        if coring == "Y":
            if Die_type == "H":
                for n in [580,650,725,830,965]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met

                    front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300
                    back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                   
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
                           
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
       
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End mm':Adjusted_Butt_End,
                        'Extrudable Weight Kg':total_Ex_Weight,
                        'front_end': front_end,
                        "back_end": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery
                    })
       
            elif Die_type == "S":
                for n in [580,650,725,830,965]:  # Iterate through n values 5, 6, 7, 8, 9
                    Billet_size = n
                    input_weight = Billet_size * 0.0876
                    total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                    total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)
                    if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met

                    front_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.3
                    back_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
                    Tolerance=front_end + back_end
                   
                    total_leng_coring = total_Ex_Length - (front_end + back_end)
                    total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
                    Total_No_of_Pcs_Mtrs=(Required_extrusion_cutlength/1000)*total_pcs_cut
                    # st.write(f"Total_No_of_Pcs_Mtrs:{Total_No_of_Pcs_Mtrs}")
                    Excess_mtrs=total_leng_coring-Total_No_of_Pcs_Mtrs
                   
       
                    # Calculate output weight and recovery
                    out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                    Recovery = (out_put / input_weight) * 100
       
                    # Check if this recovery is the maximum so far
                    if Recovery > max_recovery:
                        max_recovery = Recovery
                        best_n = n
                        best_total_pcs_can_cut = total_pcs_cut  # Update best total_pcs_can_cut
       
                    # Collect results for each n
                    results.append({
                        'Billet Length (mm)': n,
                        'Butt End mm':Adjusted_Butt_End,
                        'Extrudable Weight Kg':total_Ex_Weight,
                        'front_end': front_end,
                        "back_end": back_end,
                        'Total mtrs':total_Ex_Length,
                        'Tolerance':Tolerance,
                        'Available Mtrs':total_leng_coring,                      
                        'No_of_Pcs_to_plan': total_pcs_cut,
                        'Total No of Pcs Mtrs':Total_No_of_Pcs_Mtrs,
                        'Cut_length': Required_extrusion_cutlength,  # Store the cut length in results
                        'Excess mtrs':Excess_mtrs,                        
                        'Recovery': Recovery
                    })
       
            else:
                st.error("No input for Die type")
                return
       
            # After finding the best_n and corresponding max_recovery, use them to calculate Total_billet_required
            if best_total_pcs_can_cut > 0:
                Total_billet_required = math.ceil(total_order / (best_total_pcs_can_cut*cav))

                Billet_size = best_n
                input_weight = Billet_size * 0.0876
                total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)

               
                front_end = ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.300 if Die_type == "H" else ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300
                back_end = ((total_Ex_Weight * 0.045) / (weight_per_meter * cav)) + 0.300 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav) if Die_type == "H" else ((total_Ex_Weight * 0.09) / (weight_per_meter * cav)) + 0.3 + ((((50 - Adjusted_Butt_End) * 0.0876) / weight_per_meter) / cav)
               
                total_leng_coring = total_Ex_Length - (front_end + back_end)
                total_pcs_cut = math.floor(total_leng_coring / (Required_extrusion_cutlength / 1000))
       
                out_put = total_pcs_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                Total_output_weight = out_put * Total_billet_required
                Total_input_weight = Total_billet_required * Billet_size * 0.0876
       
                Total_recovery = (Total_output_weight / Total_input_weight) * 100
       
                df_results = pd.DataFrame(results)

                data = {
                "Parameter": [
                
                "Maximum Recovery",
                "Billet Length",
                "Total Billets Required",
                "Total Input Weight",
                "Total Output Weight",
                "Total Recovery",
                "Total Extrudable Length per Billet mtr",
                "Front end coring mtr",
                "Back end coring mtr"
                     ],
                "Value": [
                
                f"{max_recovery:.2f}%",
                f"{best_n} mm",
                f"{Total_billet_required} Nose",
                f"{Total_input_weight:.2f} kg",
                f"{Total_output_weight:.2f} kg",
                f"{Total_recovery:.2f}%",
                f"{total_Ex_Length:.3f}",
                f"{front_end:.3f}",
                f"{back_end:.3f}"
                    ]
                }

                # Create DataFrame
                df = pd.DataFrame(data)

                # Display table in Streamlit
                st.subheader("Best Optimal Results")
                st.write(df)
                # st.subheader(f"Best Optimal Results")        
                # st.write(f"Maximum Recovery: {max_recovery:.2f}% with n = {best_n}")
                # st.write(f"Total Billets Required: {Total_billet_required}")
                # st.write(f"Total Input Weight: {Total_input_weight:.3f} kg")
                # st.write(f"Total Output Weight: {Total_output_weight:.3f} kg")
                # st.write(f"Total Recovery: {Total_recovery:.3f}%")
       
                st.subheader("Results for each Billet")

                def highlight_max_adjust(row):
                    return ['background-color: lightgreen' if row.name == df_results["Recovery"].idxmax() else '' for _ in row]

                # Apply the highlighting function and display DataFrame
                st.write("Results with highlighted row for maximum Adjust value:")
                st.dataframe(df_results.style.apply(highlight_max_adjust, axis=1))
                

                st.write("\nUse when you can adjust coring tolerance less than 0.25 mtr:")
                df_new=df_results
                df_new["Adjust"]=(df_new["Excess mtrs"]-(df_new["Cut_length"]/1000))
                df_new["updated_No_of_pcs_to_plan"]=df_new["No_of_Pcs_to_plan"]+1
                out_put = df_new["updated_No_of_pcs_to_plan"] * ((df_new["Cut_length"]*cav) / 1000) * weight_per_meter
                Total_input_weight=df_new["Billet Length (mm)"]*0.0876
                df_new["Adjusted_recovery"]=(out_put/Total_input_weight)*100
                # df_new = df_new[df_new['Cut_length'] == best_cut_length]
                df_new_sort=df_new.sort_values(by="Adjust",ascending=False)

                def highlight_max_adjust(row):
                    return ['background-color: lightgreen' if row.name == df_new_sort["Adjust"].idxmax() else '' for _ in row]

                # Apply the highlighting function and display DataFrame
                st.write("Results with highlighted row for maximum Adjust value:")
                st.dataframe(df_new_sort.style.apply(highlight_max_adjust, axis=1))
       
            
       
        elif coring == "N":
            Stretch_Allowance = st.number_input("Enter Stretch_Allowance if no coring (mtr):", min_value=0.001, step=0.001, format="%.5f")
            results = []
            for n in range(500,1001,5):  # Iterate through n values 5, 6, 7, 8, 9
                Billet_size = n
                input_weight = Billet_size * 0.0876
                total_Ex_Weight = (Billet_size - Adjusted_Butt_End) * 0.0876
                total_Ex_Length = total_Ex_Weight / (weight_per_meter * cav)+0 #+2 is for stretching allowance
                if total_Ex_Length > 48:
                        continue  # Skip this iteration if the condition is not met               
                

                total_pcs_can_cut = math.floor((total_Ex_Length-Stretch_Allowance) / (Required_extrusion_cutlength / 1000))  # extrusion pcs per billet
               
                # Calculate output weight and recovery
                out_put = total_pcs_can_cut * ((Required_extrusion_cutlength*cav) / 1000) * weight_per_meter
                Recovery = (out_put / input_weight) * 100
                Total_No_of_Pcs_Mtrs=total_pcs_can_cut*(Required_extrusion_cutlength/1000)
                Excess_mtrs=total_Ex_Length-Total_No_of_Pcs_Mtrs
       
                # Check if this recovery is the maximum so far
                if Recovery > max_recovery:
                    max_recovery = Recovery
                    best_n = n
                    best_total_pcs_can_cut = total_pcs_can_cut  # Update best total_pcs_can_cut
       
                # Collect results for each n
                results.append({
                    'Billet Length (mm)': n,
                    'Butt End mm':f"{Adjusted_Butt_End:.2f}",
                    'Extrudable Weight Kg':f"{total_Ex_Weight:.2f}",
                    'Total mtrs':f"{total_Ex_Length:.2f}",             
                    'No_of_Pcs_to_plan': total_pcs_can_cut,
                    'Total No of Pcs Mtrs':f"{Total_No_of_Pcs_Mtrs:.2f}",
                    'Cut_length': f"{Required_extrusion_cutlength:.2f}",  # Store the cut length in results
                    'Excess mtrs':f"{Excess_mtrs:.2f}",                        
                    'Recovery': f"{Recovery:.2f} %"
                })
       
            # After finding the best_n and corresponding max_recovery, use them to calculate Total_billet_required
            if best_total_pcs_can_cut > 0:
                Total_billet_required = math.ceil(total_order / (best_total_pcs_can_cut*cav))

                Billet_size = best_n
                input_weight=Billet_size*0.0876
                total_Ex_Weight=(Billet_size-Adjusted_Butt_End)*0.0876
                total_Ex_Length=total_Ex_Weight/(weight_per_meter*cav)

                total_pcs_can_cut=math.floor(total_Ex_Length/(Required_extrusion_cutlength/1000))

                out_put=total_pcs_can_cut*((Required_extrusion_cutlength*cav)/1000)*weight_per_meter
                Total_output_weight = Total_billet_required * out_put
                Total_input_weight = (Total_billet_required * (Billet_size)) * 0.0876
                Total_recovery = (Total_output_weight / Total_input_weight) * 100
       
                df_results = pd.DataFrame(results)

                data = {
                "Parameter": [
                
                "Maximum Recovery",
                "Billet Length",
                "Total Billets Required",
                "Total Input Weight",
                "Total Output Weight",
                "Total Recovery",
                "Total Extrudable Length per Billet"
                     ],
                "Value": [
                
                f"{max_recovery:.2f}%",
                f"{best_n} mm",
                f"{Total_billet_required} Nose",
                f"{Total_input_weight:.2f} kg",
                f"{Total_output_weight:.2f} kg",
                f"{Total_recovery:.2f}%",
                f"{total_Ex_Length:.3f} Meter"
                    ]
                }

                # Create DataFrame
                df = pd.DataFrame(data)

                # Display table in Streamlit
                st.subheader("Best Optimal Results")
                st.write(df)
                # st.subheader(f"Best Optimal Results")
                # st.write(f"Maximum Recovery: {max_recovery:.3f}% with n = {best_n}")
                # st.write(f"Total Billets Required: {Total_billet_required}")
                # st.write(f"Total Input Weight: {Total_input_weight:.3f} kg")
                # st.write(f"Total Output Weight: {Total_output_weight:.3f} kg")
                # st.write(f"Total Recovery: {Total_recovery:.3f}%")
               
       
                # st.subheader("Results for each Billet")
                Billets = st.number_input("Enter Billet Length (mm):", min_value=500.00,step=5.00,format="%.3f")
                df_results = df_results[(df_results['Billet Length (mm)'] == Billets)]
                st.write("\nResults for selected billet length with fab passible cut_length:")
                
                def highlight_lowest_adjust(row):
                    return ['background-color: lightgreen' if val == df_results["Recovery"].max() else '' for val in row]

                # Apply the highlighting function and display DataFrame
                
                st.dataframe(df_results.style.apply(highlight_lowest_adjust, axis=1))
                
       
            else:
                st.warning("No valid total_pcs_can_cut found.")
   
    else:
        st.error("Enter valid details for Fabrication Required")


 
# Streamlit interface
def main():
    st.title('Cut Length & Recovery Optimizer')
   
    st.sidebar.title('Input Parameters')
    Die_Number = st.sidebar.number_input("Die number:", min_value=1)
    weight_per_meter = st.sidebar.number_input("Weight per meter (Kg/m):", min_value=0.00001, step=0.00001,format="%.5f")
    cav = st.sidebar.number_input("Number Of Cavity In Die:", min_value=1)
    cut_length = st.sidebar.number_input("Ordered cut length (mm):", min_value=0.001,step=0.001,format="%.5f")
    total_order = st.sidebar.number_input("Total Order Qty (Pcs):", min_value=0)
   
    Adjusted_Butt_End = st.sidebar.number_input("Enter Adjusted Butt End (mm):", min_value=0)
    Fab = st.sidebar.selectbox("Fabrication Required Y/N:", ["Y", "N"])
    coring = st.sidebar.selectbox("Is this coring section Y/N:", ["Y", "N"])
    Die_type = st.sidebar.selectbox("Enter the die type (H or S):", ["H", "S"])
    Press=st.sidebar.selectbox("Enter the Press type (Press1 or Press2):",["Press1","Press2"])
    if Press == "Press2":          
    
        if Fab == "Y" and coring in ["Y", "N"]:
            Calculate_fab_Yes_coring_yes_No(total_order, weight_per_meter, cav, Adjusted_Butt_End, Die_type, Fab, coring)
        elif Fab=="N" and coring in ["Y","N"]:
            calculate_recovery_Fab_No_coring_Yes_No(Die_Number, weight_per_meter, cav, cut_length, total_order, Adjusted_Butt_End, Fab, coring, Die_type)
        else:
            st.error("Please enter valid inputs for Fabrication and Coring sections.")
    elif Press == "Press1":
        if Fab == "Y" and coring in ["Y", "N"]:
            Calculate_fab_Yes_coring_yes_No_press1(total_order, weight_per_meter, cav, Adjusted_Butt_End, Die_type, Fab, coring)
        elif Fab=="N" and coring in ["Y","N"]:
            calculate_recovery_Fab_No_coring_Yes_No_press1(Die_Number, weight_per_meter, cav, cut_length, total_order, Adjusted_Butt_End, Fab, coring, Die_type)
        else:
            st.error("Please enter valid inputs for Fabrication and Coring sections.")
 
if __name__ == '__main__':
    main()
 
