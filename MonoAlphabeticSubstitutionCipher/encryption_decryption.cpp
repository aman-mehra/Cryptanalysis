//
// Created by Aditya Bhadoo on 30/08/20.
//

#include <bits/stdc++.h>
#include <fstream>

using namespace std;

map<string,string> lookupTable;
map<string,string> inv_lookupTable;
vector<string> plaintexts_buffer;
vector<string> ciphertexts_buffer;

// Setup key permutation
void precal(){

    srand( (unsigned)time(NULL) );
    string U[]={"a","b","c"};

    // Setting up original permutation to map from 
    vector<string> lookup;
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            lookup.push_back(U[i]+U[j]);
        }
    }
    int i=0;

    // Random key generation
    vector<string> cp=lookup;
    while(!lookup.empty()){
        string cur=cp[i++];
        int pick=rand()%lookup.size();
        lookupTable[cur]=lookup[pick];
        inv_lookupTable[lookup[pick]]=cur;
        lookup.erase(lookup.begin()+pick);
    }
}

string encrypt(string p){
    string cipher="";
    string h=to_string(hash<string>{}(p));

    for(int i=0;i<p.length()-1;i+=2){
        cipher+=lookupTable[p.substr(i,2)];
    }
    return cipher+h+to_string(h.length());
}

string decrypt(string c){
    string plainText="";
    int len=stoi(c.substr(c.length()-2))+2;
    string cipher=c.substr(0,c.length()-len);
    for(int i=0;i<cipher.length()-1;i+=2){
        plainText+=inv_lookupTable[cipher.substr(i,2)];
    }

    string encrypt_hash = c.substr(c.length()-len,len-2);
    string decrypt_hash = to_string(hash<string>{}(plainText));

    if (encrypt_hash != decrypt_hash){
        cout << "Something Is Wrong. Hash Mismatch. " << "\n" << "Hash before Encryption = " << encrypt_hash << "\n" "Hash after Decryption = " << decrypt_hash << endl;
        cout << "Decrypted " << plainText << endl;
    }

    return plainText;
}

int load_plaintexts(){
    ifstream file("input.txt");
    string line;
    while (getline(file, line)) {
         line.erase(std::find_if(line.rbegin(), line.rend(), [](int ch) {
                return !std::isspace(ch);
            }).base(), line.end());
        plaintexts_buffer.push_back(line);
    }
    // plaintexts_buffer.push_back("abcbcccacbba");
    // plaintexts_buffer.push_back("acbabbcbaacaac");
    // plaintexts_buffer.push_back("bbbcaabcccba");
    // plaintexts_buffer.push_back("bbbbaaaacbbbaa");
    // plaintexts_buffer.push_back("bccbbabcbccc");
    return 0;
}

int write_ciphertexts(){
    ofstream outfile("cipher.txt");
    for(int ind=0;ind<ciphertexts_buffer.size();ind++) {
        outfile << ciphertexts_buffer[ind];
        if(ind != ciphertexts_buffer.size())
            outfile << "\n";
    }
    return 0;
}


int main(){

    load_plaintexts();

    precal();
    for(auto x:lookupTable){
        cout<<x.first<<"->"<<x.second<<"\n";
    }
    cout<<"\ninverse\n";
    for(auto x:inv_lookupTable){
        cout<<x.first<<"->"<<x.second<<"\n";
    }

    cout << endl;

    for(int ind=0;ind<plaintexts_buffer.size();ind++){
        string plaintext=plaintexts_buffer[ind];
        string cipher=encrypt(plaintext);
        ciphertexts_buffer.push_back(cipher);
        string decrypted_plain = decrypt(cipher);
        // cout << plaintext << endl;
        cout<<"Plain text = "<<plaintext<<" --- Cipher text = "<<cipher<<" --- Decrypted text = "<< decrypted_plain << endl;
    }  
    write_ciphertexts();

    return 0;
}

