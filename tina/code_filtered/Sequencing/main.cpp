#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
using namespace std;

struct node{
    int num;
    node *next;

    node(int n){
        num = n;
        next = NULL;
    }

//    ~node(){
//        delete next;
//    }

};

struct linkedList{
    int represent;
    node *head;
    node *end;
    int size;

    linkedList(const linkedList &l){
        represent=l.represent;
//        head = l.head;
//        end = l.end;

        if(l.head==NULL){
            head = end = NULL;
        }else {

            node *reference = l.head;
            head = new node(reference->num);
            end = head;
            reference = reference->next;
            while (reference != NULL) {
                end->next = new node(reference->num);
                end = end->next;
                reference = reference->next;
            }
        }



        size = l.size;
    }

    const linkedList& operator=(const linkedList &l){
        delete head;
        represent=l.represent;
//        head = l.head;
//        end = l.end;

        if(l.head==NULL){
            head = end = NULL;
        }else {

            node *reference = l.head;
            head = new node(reference->num);
            end = head;
            reference = reference->next;
            while (reference != NULL) {
                end->next = new node(reference->num);
                end = end->next;
                reference = reference->next;
            }

        }


        size = l.size;
    }

    linkedList(){
        head=end=NULL;
        size=0;
    }
    ~linkedList(){
        delete head;
        size = 0;
    }

    linkedList(int h){
        represent=h;
        head=end=NULL;
        size=0;

    }

    void add_v(int v){

        if(size==0){
            head = new node(v);
            end = head;
        }else {
            end->next = new node(v);
            end = end->next;
        }

        size++;
    }

    bool rm_v(int v){
        node *find =head;
        if(size==0){
            return false;
        }

        if(find == end&&find->num==v){
            delete find;
            head = end =NULL;
            size--;
            return true;

        }else if(find==end){
            return false;
        }

        if(find->num==v){
            head=head->next;
            find->next=NULL;
            delete  find;
            size--;
            return true;

        }
        while(find!=end){
            if(find->next->num==v){
                node *temp = find->next;
                find->next=find->next->next;
                delete temp;
                size--;
                return true;
            }

            find=find->next;
        }

        return false;

    }

    bool operator<(const linkedList & right) const {
        if(size>=right.size){
            return false;
        }
        return true;
    }

};

int return_access_index(string[],string);
void cancel_connection(linkedList&,linkedList[]);
int return_intex_of_representitive(int representitive, linkedList[]);
int main() {
    ifstream number("C:\\Users\\LIXIA\\CLionProjects\\Sequencing\\asscession_num.txt");
    ifstream edge("C:\\Users\\LIXIA\\CLionProjects\\Sequencing\\uniqSETs.tsv");

    string arr[33];
    int i=0;

    //read in accession number into
    while(number>>arr[i]) {
        cout<<i<<"\t"<<arr[i]<<endl;
        i++;
    }

    //build the edge
    linkedList linkedLists[33] ;

    for(int i=0;i<33;i++){
        linkedLists[i].represent=i;
    }

    int index=0;
    string current_index;
    string current;
    string next;

    edge>>current;
    current_index=current;

    edge>>next;
    int a=return_access_index(arr,next);
    linkedLists[index].add_v(a);


    while(edge>>current){
        if(current!=current_index){
            index ++;
            current_index = current;
        }

        edge>>next;
        linkedLists[index].add_v(return_access_index(arr,next));
    }


    //sort based on the size
    sort(linkedLists,linkedLists+33);

    reverse(linkedLists,linkedLists+33);

    //delete by the order
    int index2=0;
    while(linkedLists[index2].size>0){
        cancel_connection(linkedLists[index2],linkedLists);
        index2++;

        sort(linkedLists+index2,linkedLists+33);
        reverse(linkedLists+index2,linkedLists+33);
    }

    for(int i=0;i<index2;i++){
        cout<<arr[linkedLists[i].represent]<<endl;
    }


    return 0;
}
void cancel_connection(linkedList &curr,linkedList l[]){

    node *f=curr.head;
    while(f!=NULL){
        int node=f->num;
        int index = return_intex_of_representitive(node,l);
        linkedList ch = l[index];
        l[index].rm_v(curr.represent);
        f=f->next;
    }

    delete curr.head;
    curr.size=0;


}
int return_intex_of_representitive(int representitive, linkedList l[]){
    int index=0;
    while(l[index].represent!=representitive){
        index++;
    }
    return index;
}

int return_access_index(string arr[],string s){
    int index = 0;
    while(arr[index]!=s){
        index++;
    }

    return index;
}



