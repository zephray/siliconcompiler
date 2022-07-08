library ieee;
use ieee.std_logic_1164.all;

entity sram_0rw1r1w_64_512_freepdk45 is
    port(
        clk0 : in std_logic;
        csb0 : in std_logic;
        wmask0 : in std_logic_vector(7 downto 0);
        addr0 : in std_logic_vector(8 downto 0);
        din0 : in std_logic_vector(63 downto 0);

        clk1 : in std_logic;
        csb1 : in std_logic;
        addr1 : in std_logic_vector(8 downto 0);
        dout1 : out std_logic_vector(63 downto 0)
        );

end sram_0rw1r1w_64_512_freepdk45;

architecture rtl of sram_0rw1r1w_64_512_freepdk45 is

begin

end;
