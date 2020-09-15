//
// Created by Aditya Bhadoo on 06/09/20.
//
#include <bits/stdc++.h>
using namespace std;

vector<string> ciphertexts;
// vector<string> plaintext_truth;

class brute_force{
public:
    string cipher;
    string hash;
    vector<map<string,string>> all_keys;
    vector<map<string,string>> all_inv_keys;

    brute_force(string c){
        string plainText="";
        int len=stoi(c.substr(c.length()-2))+2;
        string cipher=c.substr(0,c.length()-len);
        this->hash=c.substr(c.length()-len,len-2);
        this->cipher=cipher;
    }
    
    bool setup(string c){
        string plainText="";
        int len=stoi(c.substr(c.length()-2))+2;
        string cipher=c.substr(0,c.length()-len);
        this->hash=c.substr(c.length()-len,len-2);
        this->cipher=cipher;
    }

    bool check_permutation(string perm[]) {
        string original[] = {"aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"};
        map<string,string> lookup; 
        map<string,string> inv_lookup; 
        for(int i=0;i<9;i++){
            lookup[perm[i]]=original[i];
            inv_lookup[original[i]] = perm[i];
        }
        string plaintextx="";
        for(int i=0;i<cipher.length()-1;i+=2){
            plaintextx+=lookup[cipher.substr(i,2)];
        }
        string h=to_string(std::hash<string>{}(plaintextx));

        if(h==this->hash) {
            // this->key=inv_lookup;
            this->all_inv_keys.push_back(inv_lookup);
            this->all_keys.push_back(lookup);
        }
        return false;
    }

    bool permutations() {
        string lookup[] = {"aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"};
        do {
            check_permutation(lookup);
        } while (next_permutation(lookup, lookup + 9));
    }

    bool check_key(int ind){
        string candidate_plain="";
        auto test_key = all_keys[ind];

        for(int i=0;i<cipher.length()-1;i+=2){
            candidate_plain+=test_key[cipher.substr(i,2)];
        }
        string h=to_string(std::hash<string>{}(candidate_plain));

        if(h==this->hash) {
            return true;
        }

        return false;
    }

    int elimination() {
        vector<int> good_indices;
        for(int ind=0;ind<all_keys.size();ind++){
            bool match = check_key(ind);
            if(match){
                good_indices.push_back(ind);
            }
        }

        vector<map<string,string>> tmp_all_keys;
        vector<map<string,string>> tmp_all_inv_keys;

        for(int ind=0;ind<good_indices.size();ind++){
            tmp_all_keys.push_back(all_keys[good_indices[ind]]);
            tmp_all_inv_keys.push_back(all_inv_keys[good_indices[ind]]);
        }

        all_keys = tmp_all_keys;
        all_inv_keys = tmp_all_inv_keys;

        return 0;
    }

};


int read_ciphers(){
    ifstream file("cipher.txt");
    string line;
    while (getline(file, line)) {
         line.erase(std::find_if(line.rbegin(), line.rend(), [](int ch) {
                return !std::isspace(ch);
            }).base(), line.end());
        ciphertexts.push_back(line);
    }
    return 0;
}

string decrypt(map<string,string> inv_lookupTable){

    ofstream outfile("output.txt");

    for(int ind=0;ind<ciphertexts.size(); ind++){
        string c = ciphertexts[ind];
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
        else{
            cout << plainText << endl;
            outfile << plainText;
            if(ind != ciphertexts.size())
                outfile << "\n";
        }
    }
}

int main()
{
    // writeFile();
    string reference[] = {"aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"};
    read_ciphers();
    // load_plaintexts();
    brute_force bf(ciphertexts[0]);
    for(int ind=0;ind<ciphertexts.size(); ind++){
        cout << "Decrypting " << ciphertexts[ind] << "..." << endl;
        bf.setup(ciphertexts[ind]);
        if(ind==0){
            bf.permutations();
        }
        else{
            bf.elimination();
        }
        if (bf.all_keys.size()>0){
            cout << "Total Keys Present = " << bf.all_keys.size() << endl;
        }else
            cerr<<"not  able  to  crack  it\n";
    }
    for(int ind=0;ind<bf.all_inv_keys.size(); ind++){
        cout << "Matched key " << ind+1 << endl;
        auto cor_key = bf.all_inv_keys[ind];
        for(int ord=0;ord<9;ord++)
            cout<<reference[ord]<<"->"<<cor_key[reference[ord]]<<"\n";
        cout << "\nDecrypted plaintext\n"<< endl;   
        decrypt(bf.all_keys[ind]);
    }
    return 0;   
}

